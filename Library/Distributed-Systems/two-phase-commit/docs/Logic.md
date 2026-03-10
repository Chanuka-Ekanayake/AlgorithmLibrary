# Two-Phase Commit (2PC) Logic

## 1. Introduction
The Two-Phase Commit (2PC) protocol is a classic distributed algorithm used to ensure all participants in a distributed transaction either entirely commit the transaction or entirely abort it. It provides Atomicity in the ACID properties for distributed systems. The protocol is resilient against certain types of node and network failures and ensures data consistency across multiple independent databases or resource managers.

### Key Roles
- **Coordinator:** The central node that orchestrates the transaction. It receives the transaction request, drives both phases of the protocol, and makes the final commit/abort decision.
- **Participants (Resource Managers):** The individual databases, services, or storage nodes that hold the actual data and execute the local operations.

---

## 2. The Two Phases of the Protocol

The protocol is split into two distinct phases to ensure that no node commits unless all nodes are ready to commit.

### Phase 1: The Prepare Phase (Voting Phase)

The purpose of this phase is for the Coordinator to ask all Participants if they are prepared to execute the transaction and commit to its outcome.

1. **Transaction Start:** The Coordinator receives a distributed transaction request containing a set of operations to be performed on the Participants.
2. **Send Prepare:** The Coordinator assigns a unique Transaction ID and sends a `PREPARE` message along with the transaction payload to all participating nodes.
3. **Local Evaluation:**
   - Each Participant receives the `PREPARE` request.
   - The Participant evaluates the transaction locally. This involves checking constraints, acquiring necessary locks (e.g., write locks), writing to a write-ahead log (WAL) for durability, and determining if the operation can succeed.
4. **Voting:**
   - If the Participant determines it can successfully commit the transaction without violating constraints, it moves to the `READY` state and sends a `VOTE_COMMIT` message back to the Coordinator.
   - If the Participant cannot execute the transaction (e.g., inadequate funds, lock timeout, constraint violation), it moves to the `ABORTED` state and sends a `VOTE_ABORT` message to the Coordinator.

### Phase 2: The Commit Phase (Completion Phase)

The purpose of this phase is for the Coordinator to make a final decision based on the votes and propagate that decision to all Participants.

1. **Decision Making:**
   - The Coordinator waits for votes from all Participants.
   - **Case A (All Commit):** If the Coordinator receives `VOTE_COMMIT` from *every* Participant, it decides to globally commit the transaction. It logs the `GLOBAL_COMMIT` decision to its own durable storage.
   - **Case B (Any Abort or Timeout):** If the Coordinator receives at least one `VOTE_ABORT` message, or if one or more Participants fail to respond within a specified timeout period, the Coordinator decides to globally abort the transaction. It logs the `GLOBAL_ABORT` decision.
2. **Propagate Decision:**
   - The Coordinator sends the final decision (`GLOBAL_COMMIT` or `GLOBAL_ABORT`) to all Participants.
3. **Local Resolution:**
   - **On Global Commit:** Participants receiving `GLOBAL_COMMIT` apply the changes to their local database, release the previously acquired locks, mark the transaction as `COMMITTED`, and optionally send an acknowledgment back to the Coordinator.
   - **On Global Abort:** Participants receiving `GLOBAL_ABORT` rollback any temporary changes made during the Prepare Phase, release the locks, mark the transaction as `ABORTED`, and acknowledge the Coordinator.
4. **Finalization:**
   - Once the Coordinator receives acknowledgments from all Participants, the distributed transaction is officially complete, and the Coordinator can reclaim resources related to the transaction.

---

## 3. Node States

Understanding the state transitions of the nodes is critical to implementing and debugging 2PC.

### Participant States
- **INIT:** The initial state before a transaction begins.
- **READY:** The Participant has successfully evaluated the `PREPARE` request, written to its local log, and voted to commit. It is now waiting for the final decision. This is a *blocking state*; the Participant holds locks and cannot proceed until the Coordinator sends the final decision.
- **COMMITTED:** The final state where changes are permanently applied.
- **ABORTED:** The final state where changes are rolled back.

### Coordinator States
- **INIT:** Preparing to broadcast the transaction.
- **WAITING:** Sent `PREPARE` to all Participants and is currently awaiting their votes.
- **COMMITTED:** All Participants voted to commit, and the global decision is to commit.
- **ABORTED:** At least one Participant voted to abort or timed out, and the global decision is to abort.

---

## 4. Failure Scenarios and Recovery

Two-Phase Commit must handle various network and node failures. Here is how standard 2PC handles common issues:

### Participant Failures
- **Failure before Voting:** If a Participant fails and does not send a vote, the Coordinator will eventually time out while in the `WAITING` state and send a `GLOBAL_ABORT` to the other Participants.
- **Failure after Voting "Commit":** If a Participant votes `VOTE_COMMIT`, enters the `READY` state, and then crashes before receiving the global decision, it must recover its state upon reboot. During recovery, it reads its Write-Ahead Log, realizes it is in the `READY` state for a specific transaction, and must query the Coordinator to find out the final decision.
- **Failure after receiving Decision:** If a Participant receives the global decision but crashes before executing it or sending an acknowledgment, it will re-execute the decision upon recovery since the Coordinator will keep resending the decision until acknowledged.

### Coordinator Failures
- **Failure before Phase 1:** The transaction simply does not start. Client receives an error.
- **Failure during Phase 1 (before Decision):** The Coordinator fails while waiting for votes. Participants sitting in the `READY` state are indefinitely blocked. This is the **major flaw** of 2PC. Since participants hold locks, the system grinds to a halt. When the Coordinator recovers, it can restart the protocol or abort.
- **Failure after Decision:** The Coordinator decides to `GLOBAL_COMMIT` and saves the decision to its log but crashes before sending the message to all Participants. Again, Participants in the `READY` state are blocked. Upon Coordinator recovery, it reads its log and resends the `GLOBAL_COMMIT` message to all Participants.

---

## 5. Algorithmic Pseudocode

### Coordinator Logic
```python
def execute_transaction(tx):
    # Phase 1
    log("PREPARE tx")
    for p in participants:
         send_prepare(p, tx)
    
    votes = wait_for_all_votes(timeout)
    
    # Phase 2
    if all_votes_are_commit(votes):
         log("GLOBAL_COMMIT tx")
         for p in participants:
             send_commit(p, tx)
         return SUCCESS
    else:
         log("GLOBAL_ABORT tx")
         for p in participants:
             send_abort(p, tx)
         return FAILURE
```

### Participant Logic
```python
def on_receive_prepare(tx):
    success = local_evaluate_and_lock(tx)
    if success:
         log("READY tx")
         send_vote_commit(coordinator, tx)
    else:
         log("ABORTED tx")
         send_vote_abort(coordinator, tx)

def on_receive_global_commit(tx):
    apply_changes(tx)
    release_locks(tx)
    log("COMMITTED tx")
    send_ack(coordinator, tx)

def on_receive_global_abort(tx):
    rollback_changes(tx)
    release_locks(tx)
    log("ABORTED tx")
    send_ack(coordinator, tx)
```

## 6. Limitations of Two-Phase Commit

While 2PC provides strict Atomicity, it carries a few significant downsides:
1. **Blocking Protocol:** The biggest issue. If the Coordinator fails after participants move to the `READY` state, those participants remain blocked indefinitely holding locks.
2. **Performance Spikes:** Requires multiple network round trips and durable disk writes (fsync) per transaction, making it very slow compared to local transactions.
3. **Scalability Bottleneck:** Since it locks resources across distributed nodes for the duration of the network calls, throughput can degrade significantly unscaled systems. It does not scale well over Wide Area Networks (WANs).

Because of these limitations, modern distributed systems sometimes favor eventual consistency patterns like **Sagas** or consensus protocols like **Paxos/Raft**, or Three-Phase Commit (3PC), which aims to solve the blocking problem.