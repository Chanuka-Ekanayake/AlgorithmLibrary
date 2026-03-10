# Two-Phase Commit (2PC) Algorithm Library

Welcome to the Two-Phase Commit (2PC) implementation for the Distributed Systems Algorithm Library.

## Overview

The **Two-Phase Commit (2PC)** is a distributed algorithm that coordinates all the processes that participate in a distributed atomic transaction on whether to commit or abort (roll back) the transaction. It is widely used in distributed database systems to ensure consistency across multiple distinct data stores.

This implementation provides a clear, documented, and fully tested Python version of the 2PC algorithm, including both the **Transaction Coordinator** and **Participant** roles.

## File Structure

The project is structured into three main directories:

- **`core/`**: Contains the core Python implementation.
  - `two_phase_commit.py`: The executable code defining the `Coordinator`, `Participant`, and the message flow.
- **`docs/`**: Contains theoretical definitions and complexity analysis.
  - `Logic.md`: Explains the algorithm step-by-step, including states (Prepare and Commit phases).
  - `Complexity.md`: Discusses Message Complexity, Time/Latency Cost, and Space overhead in a distributed context.
- **`test-project/`**: Contains unit and integration tests.
  - `test_two_phase_commit.py`: Extensive test suite using `unittest` combined with mocking to test failures and edge cases.

---

## How it Works

The algorithm consists of two phases:

### Phase 1: The Prepare Phase (Voting)
The Coordinator sends a `PREPARE` request to all participants containing the transaction payload.
Each Participant evaluates the transaction locally (verifying if constraints are met, acquiring locks, etc).
- If the Participant determines it can commit the transaction, it responds with `VOTE_COMMIT` and enters the `READY` state.
- If the Participant cannot process the transaction, it returns `VOTE_ABORT` and terminates.

### Phase 2: The Commit Phase (Completion)
The Coordinator waits for responses from all participants.
- **Global Commit:** If *all* participants return `VOTE_COMMIT`, the Coordinator decides to commit the transaction and broadcasts `GLOBAL_COMMIT` to all nodes. The nodes apply the changes and release locks.
- **Global Abort:** If *any* participant returns `VOTE_ABORT` or simply times out, the Coordinator decides to abort the transaction and broadcasts `GLOBAL_ABORT` to all nodes. Any nodes in the `READY` state rollback their changes and release locks.

---

## Quick Start & Usage

### 1. Running the Core Example

The `core/two_phase_commit.py` file includes a runnable example at the bottom of the script.

```bash
python3 core/two_phase_commit.py
```

**Expected Output:**
```
2026-03-10 21:00:00 [INFO] Coordinator-Coord-1: Registered Participant: Database-Node-A
2026-03-10 21:00:00 [INFO] Coordinator-Coord-1: Registered Participant: Database-Node-B
2026-03-10 21:00:00 [INFO] Coordinator-Coord-1: Registered Participant: Message-Queue-Node
2026-03-10 21:00:00 [INFO] Coordinator-Coord-1: --- Starting Transaction TX-1001 ---
2026-03-10 21:00:00 [INFO] Coordinator-Coord-1: --- PHASE 1: PREPARE ---
2026-03-10 21:00:00 [INFO] Participant-Database-Node-A: Received PREPARE for TX: TX-1001
2026-03-10 21:00:00 [INFO] Participant-Database-Node-A: Local operations successful. Voting COMMIT for TX: TX-1001
2026-03-10 21:00:00 [INFO] Coordinator-Coord-1: Received VOTE_COMMIT from Database-Node-A
...
2026-03-10 21:00:01 [INFO] Coordinator-Coord-1: --- PHASE 2: RESOLUTION ---
2026-03-10 21:00:01 [INFO] Coordinator-Coord-1: All participants voted COMMIT. Proceeding with GLOBAL_COMMIT for TX: TX-1001
2026-03-10 21:00:01 [INFO] Participant-Database-Node-A: Received global decision GLOBAL_COMMIT for TX: TX-1001
2026-03-10 21:00:01 [INFO] Participant-Database-Node-A: Committing transaction TX-1001 locally.
...
```

### 2. Understanding the Classes

If you import this in your own project, it acts as a lightweight simulator:

```python
from core.two_phase_commit import Coordinator, Participant

coord = Coordinator("My-Coordinator")
p1 = Participant("My-SQL-DB")
p2 = Participant("My-NoSQL-DB", simulate_failure_rate=0.1) # 10% chance to fail Phase 1

coord.register_participant(p1)
coord.register_participant(p2)

success = coord.execute_transaction("Tx-999", {"amount": 500})
if success:
    print("Transaction Globally Committed")
else:
    print("Transaction Globally Aborted")
```

---

## Testing

The project is highly tested. The robust test suite verifies the transaction protocol across a series of happy and failed scenarios, including simulated network failures.

**Run the tests using standard `unittest` module:**

```bash
python3 -m unittest test-project/test_two_phase_commit.py
```

The tests will silently pass, though they log the unrecoverable exception catching if un-patched.

---

## Algorithmic Limitations

It is critical to learn the limitations of this protocol:
1. **The Blocking Problem:** If the Coordinator node crashes after participants have voted `COMMIT` but before they receive the `GLOBAL_COMMIT`, those participants are stuck in a `READY` state and cannot release their database locks until the coordinator recovers. This severely throttles database throughput.
2. **Network Overhead:** Requires 2 full network round-trips plus synchronous fsync writes to disk for every participating node, leading to major performance degradation in high volume systems. 

For modern scalability, microservice architectures often replace Two-Phase Commit with the **Sagas Pattern** or consensus loops via **Raft/Paxos**.
