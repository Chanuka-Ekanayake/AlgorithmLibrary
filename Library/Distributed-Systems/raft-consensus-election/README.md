# Raft Consensus (Leader Election)

## 1. Overview

The **Raft Consensus** module is a distributed state machine designed for **Fault Tolerance** and **Strong Consistency**. In a 2026 software environment, a single server is a single point of failure. Raft allows a cluster of servers to act as a single, unified system by electing a "Leader" to coordinate all operations.

If the Leader crashes, the remaining nodes detect the failure and automatically hold a new election to restore the cluster's stability without human intervention.

---

## 2. Technical Features

- **Strong Leader Safety:** Guaranteed by the protocol to have at most one leader per "Term," preventing data corruption from "Split-Brain" scenarios.
- **Logical Clocks (Terms):** Uses monotonically increasing terms to detect and depose stale leaders and synchronize global state.
- **Quorum-Based Authority:** All transitions require a majority vote (a quorum of ⌊N/2⌋ + 1 nodes in an N-node cluster; see `docs/logic.md`), ensuring that a minority of failed nodes cannot bring down the entire system.
- **Randomized Election Jitter:** Implements randomized timeouts (150ms–300ms) to significantly reduce the probability of "Split Votes" and ensure rapid leader recovery.

---

## 3. Architecture

```text
.
├── core/                  # Distributed State Machine
│   ├── __init__.py        # Package initialization
│   └── raft_node.py       # Follower, Candidate, and Leader logic
├── docs/                  # Technical Documentation
│   ├── logic.md           # Terms, Quorums, and "Split-Brain" prevention
│   └── complexity.md      # Message overhead and fault-tolerance limits
├── test-project/          # Cluster Chaos Simulator
│   ├── app.py             # Multi-threaded cluster simulator with leader failure
│   └── instructions.md    # Guide for auditing the election lifecycle
└── README.md              # Documentation Entry Point

```

---

## 4. Performance Specifications

| Metric                 | Specification                                   |
| ---------------------- | ----------------------------------------------- |
| **Safety Property**    | Linearizability (Strong Consistency)            |
| **Fault Tolerance**    | Survives failures in a cluster                  |
| **Election Speed**     | Typically 150–300 ms (≈1–2 RTTs) for leader election under normal conditions |
| **Message Complexity** | O(n) messages during election; O(1) messages per client operation during stability |
| **State Storage**      | Volatile (Simulated) / Persistent (Logic Ready) |

---

## 5. Deployment & Usage

### Integration

The `RaftNode` is designed to be integrated into distributed service discovery or configuration management tools:

```python
from core.raft_node import RaftNode

# Initialize a node with its ID and a list of its peers
my_id = 0
peer_ids = [1, 2, 3, 4]
node = RaftNode(node_id=my_id, peer_ids=peer_ids)

# In your main event loop
while True:
    node.tick() # Checks for timeouts and manages state

```

### Running the Simulator

To see the "Leader Election" in action and witness a cluster "self-heal" after a crash:

1. Navigate to the `test-project` directory:

```bash
cd test-project

```

2. Run the Chaos Simulator:

```bash
python app.py

```

---

## 6. Industrial Applications

- **Distributed Key-Value Stores:** Powering the backend of **etcd** (used by Kubernetes) and **Consul**.
- **Database Management:** Coordinating leaders in **CockroachDB**, **MongoDB**, and **TiDB**.
- **Service Discovery:** Ensuring consistent registration of microservices in high-scale cloud environments.
- **Log Replication:** The foundation for distributed logs like those in **Apache Pulsar**.
