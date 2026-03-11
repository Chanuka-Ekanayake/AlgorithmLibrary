# Three-Phase Commit (3PC) Algorithm Library

Welcome to the Three-Phase Commit (3PC) implementation for the Distributed Systems Algorithm Library.

## Overview

The **Three-Phase Commit (3PC)** is a distributed consensus algorithm that acts as an extension to the classic Two-Phase Commit (2PC) protocol. It was designed primarily to eliminate the "blocking problem" inherent in 2PC. By introducing a new intermediate phase ("Pre-Commit") and relying on strict timeouts, 3PC enables nodes to safely recover from a coordinator crash without blocking indefinitely.

This implementation provides a clear, documented, and fully tested Python version of the 3PC algorithm, including both the **Transaction Coordinator** and **Participant** roles.

## File Structure

The project is structured into three main directories:

- **`core/`**: Contains the core Python implementation.
  - `three_phase_commit.py`: The executable code defining the `Coordinator`, `Participant`, and the three phases of message flows (`CAN_COMMIT`, `PRE_COMMIT`, `DO_COMMIT`).
- **`docs/`**: Contains theoretical definitions and complexity analysis.
  - `Logic.md`: Explains the algorithm step-by-step and how it solves the 2PC blocking problem.
  - `Complexity.md`: Discusses Message Complexity, Latency (3 Network RTTs), and why its vulnerability to Network Partitions makes it unfavorable in modern systems.
- **`test-project/`**: Contains unit and integration tests.
  - `test_three_phase_commit.py`: Extensive test suite using `unittest` combined with mocking to test timeouts, Phase 1 rejections, and Phase 2 crashes.

---

## How it Works

The algorithm consists of three distinct phases:

### Phase 1: The Voting Phase (CanCommit)
The Coordinator sends a `CAN_COMMIT` request to all participants containing the transaction payload.
Each Participant evaluates if it *can* safely commit the transaction under current local constraints.
- Responds with `VOTE_YES` or `VOTE_NO`.

### Phase 2: The Preparation Phase (PreCommit)
The Coordinator tallies the votes.
- **Global Intent to Commit:** If *all* participants return `VOTE_YES`, the Coordinator transitions to `PRECOMMIT` and broadcasts a `PRE_COMMIT` message. Participants acknowledge it with `ACK`.
- **Global Abort:** If *any* participant returns `VOTE_NO` or times out, the Coordinator broadcasts `ABORT`.

*Why is Phase 2 important?* It guarantees that before any single node commits, every other node in the system knows that every other node voted YES. 

### Phase 3: The Execution Phase (DoCommit)
The Coordinator waits for `ACK` responses.
- **Global Commit:** Once all ACKs are received, the Coordinator writes the commit intention to disk and broadcasts `DO_COMMIT`. Data is permanently written and locks are released by participants.

---

## Quick Start & Usage

### 1. Running the Core Example

The `core/three_phase_commit.py` file includes a runnable example demonstrating both a happy path and a failure path.

```bash
python3 core/three_phase_commit.py
```

**Expected Output (Snippet):**
```
--- TEST: Happy Path ---
2026-03-11 [INFO] Coordinator-Coord-1: === Starting 3PC Transaction TX-100 ===
2026-03-11 [INFO] Coordinator-Coord-1: >>> PHASE 1: CAN COMMIT
2026-03-11 [INFO] Participant-Node-A: Received CAN_COMMIT for TX: TX-100
2026-03-11 [INFO] Participant-Node-A: Local checks passed. Voting YES for TX: TX-100
...
2026-03-11 [INFO] Coordinator-Coord-1: >>> PHASE 2: PRE COMMIT
2026-03-11 [INFO] Participant-Node-A: Received PRE_COMMIT for TX: TX-100
2026-03-11 [INFO] Participant-Node-A: Entered PRECOMMIT state. Sending ACK.
...
2026-03-11 [INFO] Coordinator-Coord-1: >>> PHASE 3: DO COMMIT
2026-03-11 [INFO] Participant-Node-A: Received decision DO_COMMIT for TX: TX-100
2026-03-11 [INFO] Participant-Node-A: Executing DO_COMMIT locally. Applying changes.
2026-03-11 [INFO] Coordinator-Coord-1: === Transaction TX-100 Completed Successfully ===
```

### 2. Understanding the Classes

Incorporating it into a distributed mock application:

```python
from core.three_phase_commit import Coordinator, Participant

coord = Coordinator("My-Cluster-Coordinator")
p1 = Participant("Data-Node-1")
p2 = Participant("Data-Node-2", failure_rate_p1=0.05) # 5% chance to vote NO

coord.register_participant(p1)
coord.register_participant(p2)

# execute_transaction blocks and orchestrates the 3 phases
success = coord.execute_transaction("tx-555", {"action": "update_balance", "val": 100})
if success:
    print("3PC Succeeded!")
else:
    print("3PC Aborted.")
```

---

## Testing

The project is highly tested. The test suite validates states, exception handling, and simulated timeouts across phases.

**Run the tests using standard `unittest` module:**

```bash
python3 -m unittest test-project/test_three_phase_commit.py
```

---

## Algorithmic Limitations

While 3PC theoretically solves the Coordinator Crash Blocking problem, it introduces two fatal flaws:
1. **Network Partitions (Split-Brain):** Because 3PC relies entirely on strict timeouts to deduce failures, it cannot safely handle network partitions. If a network partition occurs during Phase 2, nodes on one side may abort while nodes on the other side commit, destroying dataset integrity. 
2. **Performance (Latency):** 3PC demands minimum **3 full Network Round-Trips** and 3 disk `fsync()` operations per node. This overhead is incredibly slow over Wide Area Networks (WANs).

Due to these flaws, modern massive-scale databases rarely use 3PC, opting instead for **Raft**, **Paxos**, or **Sagas**, or simply accepting the edge-case blocking flaw of **2PC**.
