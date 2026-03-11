# Three-Phase Commit (3PC) Logic

## 1. Introduction
The Three-Phase Commit (3PC) protocol is an extension of the Two-Phase Commit (2PC) protocol designed primarily to overcome the major flaw of 2PC: the **blocking problem**. Developed by Dale Skeen in 1981, it introduces an additional phase and a timeout mechanism to ensure that the protocol is non-blocking under fail-stop assumptions (specifically, it assumes network partitions do not occur or bounds on message delivery are strictly known).

In 2PC, if the Coordinator fails after participants have voted but before they receive the final decision, participants holding locks on resources are left in an indefinite wait state. 3PC solves this by requiring all nodes to enter a "Pre-Commit" state before actually committing.

---

## 2. The Three Phases of the Protocol

The protocol is divided into three distinct phases: CanCommit, PreCommit, and DoCommit.

### Phase 1: The Voting Phase (CanCommit)

The goal of Phase 1 is identical to the first phase of 2PC: determine if all nodes *can* commit the transaction.

1. **Transaction Request:** The Coordinator receives a distributed transaction.
2. **Send CanCommit:** The Coordinator sends a `CAN_COMMIT` message (along with the necessary transaction data) to all Participants.
3. **Local Evaluation:** Each Participant evaluates the request locally to ensure it holds the necessary resources, data constraints are met, and writes to its local logs.
4. **Voting:**
   - If the Participant can successfully prepare the transaction, it transitions to the `READY` state and replies with a `VOTE_YES`.
   - If the Participant cannot process it, it transitions to `ABORTED` and replies with a `VOTE_NO`.

### Phase 2: The Preparation Phase (PreCommit)

This is the newly added phase that distinguishes 3PC from 2PC. Its purpose is to communicate the *intention* of the final decision to all participants *before* that decision is inextricably executed.

1. **Decision Making:** The Coordinator waits for all votes.
   - **Case A (All Yes):** If the Coordinator receives `VOTE_YES` from all participants, it transitions to the `PRECOMMIT` state and broadcasts a `PRE_COMMIT` message to all participants.
   - **Case B (Any No or Timeout):** If the Coordinator receives a `VOTE_NO` or times out waiting for votes, it transitions to `ABORTED` and broadcasts an `ABORT` message.
2. **Participant Response:** 
   - Upon receiving `PRE_COMMIT`, the Participant transitions into the `PRECOMMIT` state. This signifies that the participant now knows that *all other participants voted yes*.
   - The Participant replies with an `ACK` (acknowledgement) back to the Coordinator.

### Phase 3: The Execution Phase (DoCommit)

This phase finalizes the transaction. No new decisions are made here; it strictly executes the intention built up in Phase 2.

1. **Final Decision:** The Coordinator waits for `ACK` messages from all participants in response to the `PRE_COMMIT`.
   - Once all `ACK`s are received, the Coordinator writes the `COMMIT` record to its durable log, transitions to the `COMMITTED` state, and sends a `DO_COMMIT` message to all participants.
   - If the Coordinator times out waiting for an `ACK`, it can either safely abort or rely on recovery protocols because no node has committed yet. In classic 3PC, it often aborts if not all ACKs are received.
2. **Participant Execution:**
   - Upon receiving `DO_COMMIT`, the Participant applies the transaction to its local storage, releases all locks held since Phase 1, transitions to `COMMITTED`, and sends a final `ACK`.

---

## 3. Node States

### Participant States
- **INIT:** The baseline state upon startup.
- **WAIT_VOTE:** Participant has received `CAN_COMMIT` and is deciding its vote.
- **READY:** The Participant voted `YES`. It is waiting to hear the global intention.
- **PRECOMMIT:** *[New in 3PC]* The Participant received `PRE_COMMIT`. It knows all nodes agreed to commit, but it hasn't applied the changes yet.
- **COMMITTED:** Changes applied, locks released.
- **ABORTED:** Changes rolled back, locks released.

### Coordinator States
- **INIT:** Ready to begin.
- **WAIT_VOTE:** Waiting for `VOTE_YES` / `VOTE_NO`.
- **PRECOMMIT:** *[New in 3PC]* Waiting for `ACK`s confirming all nodes received the intention to commit.
- **COMMITTED:** Transaction finalized as a success.
- **ABORTED:** Transaction finalized as a failure.

---

## 4. How 3PC Solves the Blocking Problem

In 2PC, if a participant is in the `READY` state and the Coordinator crashes, it doesn't know if the Coordinator sent `COMMIT` to other nodes before crashing, or if it was about to send `ABORT`, or if it even finished deciding. It must block indefinitely.

In 3PC, the `PRECOMMIT` state acts as a safety buffer:
- **Rule 1:** No node can enter the `COMMITTED` state until *every* node has reached the `READY` state. 
- **Rule 2:** By adding the `PRE_COMMIT` message, a node entering the `PRECOMMIT` state *knows* that every other node in the system voted `YES`.
- **Recovery Scenario A (Participant times out waiting for DO_COMMIT):** If a Participant is in the `PRECOMMIT` state and the Coordinator crashes, the Participant *knows* that there was a unanimous `YES` vote. It can safely go ahead and commit the transaction (or a newly elected Coordinator can tell everyone to commit) because no node could possibly be in the `ABORTED` state.
- **Recovery Scenario B (Participant times out waiting for PRE_COMMIT):** If a Participant is in the `READY` state and the Coordinator crashes, the Participant does *not* know the global vote. However, because no node could have received a `DO_COMMIT` (since no node even received a `PRE_COMMIT`), the Participant (or a new Coordinator) can safely *abort* the transaction.

By cleanly separating the "knowledge of unanimity" from the "execution of commit", 3PC eliminates the states of uncertainty that cause blocking in 2PC.

---

## 5. Limitations of Three-Phase Commit

Despite solving the theoretical blocking problem under specific assumptions, 3PC is rarely used in massive production systems because:
1. **Network Partition Vulnerability:** The protocol relies heavily on accurate timeouts. If a network partition occurs (Node A can't talk to Node B, but both are alive), the protocol can violently fail. One side of the partition might assume the Coordinator crashed and proceed to abort, while the other side proceeds to commit, leading to a split-brain (inconsistent data).
2. **Performance Degradation:** 2PC already adds severe latency due to 2 RTTs. 3PC demands 3 full Network RTTs (CanCommit, PreCommit, DoCommit) and at least 3 durable disk writes per participant. The latency cost is prohibitive for high-throughput databases.

For this reason, systems either tolerate the blocking flaw of 2PC (like PostgreSQL/MySQL XA transactions) or adopt Paxos/Raft for strict consensus without 3PC's vulnerabilities.