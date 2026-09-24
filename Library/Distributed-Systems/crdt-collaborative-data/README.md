# CRDT (Conflict-free Replicated Data Type)

## 1. Overview

A **Conflict-free Replicated Data Type (CRDT)** is a family of data structures that can be replicated across multiple nodes in a distributed system, updated independently and concurrently without any coordination, and **mathematically guaranteed** to converge to the same state when all updates are eventually delivered.

Unlike consensus protocols (Raft, Paxos) that require a leader and quorum to agree on writes, CRDTs achieve **Strong Eventual Consistency** through pure mathematics: their merge operations form a **Join-Semilattice**, ensuring that no matter the order updates arrive, the final state is always identical. This is the architectural foundation of **Figma**, **Apple Notes**, **Redis CRDTs**, and the entire **local-first software** movement.

---

## 2. Technical Features

- **No Coordination Required:** Unlike Raft or 2PC, nodes never need to "ask permission" to write. Every replica can accept writes immediately, even while offline.
- **Mathematical Convergence:** The merge function is **commutative**, **associative**, and **idempotent** — guaranteeing that replicas always converge regardless of message ordering, duplication, or delay.
- **Offline-First Architecture:** Devices can operate fully disconnected, accumulate changes, and seamlessly merge when connectivity resumes. Zero conflicts, zero data loss.
- **Multiple CRDT Primitives:** This package implements four foundational types:
  - **G-Counter:** Grow-only distributed counter (e.g., view counts)
  - **PN-Counter:** Increment/decrement counter built on two G-Counters
  - **LWW-Register:** Last-Writer-Wins register for single-value fields
  - **OR-Set (Observed-Remove Set):** Add/remove set with conflict-free semantics

---

## 3. Architecture

```text
.
├── core/                  # CRDT Primitives Engine
│   ├── __init__.py        # Package initialization
│   └── crdt.py            # G-Counter, PN-Counter, LWW-Register, OR-Set
├── docs/                  # Technical Documentation
│   ├── logic.md           # Semilattice theory & merge semantics
│   └── complexity.md      # Analysis of convergence & space trade-offs
├── test-project/          # The Collaborative Shopping List
│   ├── app.py             # Multi-device offline sync simulation
│   └── instructions.md    # Guide for observing conflict-free merges
└── README.md              # Documentation Entry Point

```

---

## 4. Performance Specifications

| Metric                | Specification                                       |
| --------------------- | --------------------------------------------------- |
| **Consistency Model** | Strong Eventual Consistency (SEC)                   |
| **Coordination**      | Zero (No leader, no quorum, no locking)             |
| **Merge Latency**     | O(n) where n = state size per replica               |
| **Conflict Rate**     | 0% (Conflicts are impossible by mathematical proof) |
| **Offline Support**   | Full (Unbounded offline operation)                  |

---

## 5. Deployment & Usage

### Integration

CRDTs are ideal for collaborative editing, distributed counters, and any system requiring offline-first writes:

```python
from core.crdt import GCounter, PNCounter, LWWRegister, ORSet

# Distributed page-view counter across 3 CDN edge nodes
counter_node_a = GCounter("edge-us")
counter_node_b = GCounter("edge-eu")

counter_node_a.increment(5)  # 5 views hit US edge
counter_node_b.increment(3)  # 3 views hit EU edge

# Later, merge without coordination
counter_node_a.merge(counter_node_b)
print(counter_node_a.value())  # 8 — perfectly converged

# Collaborative set (e.g., shared shopping list)
alice = ORSet("alice")
bob = ORSet("bob")

alice.add("Milk")
bob.add("Eggs")
bob.add("Milk")
bob.remove("Milk")  # Bob removes Milk — but Alice's concurrent add wins!

alice.merge(bob)
bob.merge(alice)
# Both see: {"Milk", "Eggs"} — add wins over remove (OR-Set semantics)
```

### Running the Simulator

To witness three devices collaborating on a shared shopping list — fully offline, with zero conflicts:

1. Navigate to the `test-project` directory:

```bash
cd test-project

```

2. Run the simulation:

```bash
python app.py

```

---

## 6. Industrial Applications

- **Real-time Collaboration:** Powering the multiplayer engine behind **Figma**, **Notion**, and **Apple Notes** for seamless co-editing.
- **Distributed Databases:** Conflict-free replication in **Redis CRDTs (CRDBs)**, **Riak**, and **Azure Cosmos DB**.
- **Mobile & IoT:** Offline-first data sync for mobile apps (**Ink & Switch's Automerge**, **Yjs**) and IoT sensor networks.
- **Gaming:** Shared game state in massively multiplayer environments without central server bottlenecks.
- **E-commerce:** Distributed shopping cart that never loses items, even during network partitions.
