# Paxos Consensus Algorithm

## 1. Overview

As backend systems scale to handle global traffic—such as processing concurrent transactions for software licenses or ML models across multiple continents—relying on a single database introduces a critical single point of failure. Distributed databases solve this, but introduce a massive new problem: **Consensus**.

If two users attempt to purchase the exact same digital asset at the exact same millisecond, and a network cable is severed halfway through the transaction, how do the distributed database nodes agree on who actually made the purchase?

**Paxos** is the foundational mathematical algorithm that solves this. It guarantees that a cluster of independent, asynchronous machines will agree on a single sequence of events (a single source of truth), even in the presence of massive network delays, dropped packets, and catastrophic server crashes.

---

## 2. Technical Features

- **Strict Two-Phase Commit:** Implements a rigorous `PREPARE` and `ACCEPT` protocol. Proposers must gather intelligence and secure promises from the cluster before attempting to write data, mathematically preventing split-brain data corruption.
- **Quorum Enforcement:** Operations only proceed when a strict majority (⌊N/2⌋ + 1) of nodes agree. This ensures that any two successful quorums will always overlap by at least one node, making it impossible for the cluster to accidentally accept two conflicting values.
- **Dynamic Value Adoption:** If a Proposer discovers during Phase 1 that the cluster has already begun accepting a different value from a competing transaction, it abandons its own data and helps finalize the existing data, sacrificing individual liveness to guarantee cluster-wide safety.
- **High Fault Tolerance:** A cluster of **N** nodes can seamlessly survive **F** simultaneous node failures, where **N = 2F + 1**, without dropping a transaction or corrupting the state.

---

## 3. Architecture

```text
.
├── core/                  # Distributed Systems Engine
│   ├── __init__.py        # Package initialization
│   └── paxos.py           # Acceptor and Proposer role logic
├── docs/                  # Technical Documentation
│   ├── logic.md           # The Two-Phase commit (Prepare/Accept) logic
│   └── complexity.md      # Message complexity and fault tolerance (2F+1)
├── test-project/          # Distributed Database Consensus Simulator
│   ├── app.py             # Simulates network drops and dueling proposers
│   └── instructions.md    # Guide for evaluating fault tolerance
└── README.md              # Documentation Entry Point

```

---

## 4. Performance Specifications

| Metric                  | Specification                                                                 |
| ----------------------- | ----------------------------------------------------------------------------- |
| **Network Complexity**  | N messages per phase (2N messages total), where N is the number of acceptors |
| **Optimal Speed**       | 2 Round Trip Times (RTT) to achieve consensus                                 |
| **Fault Tolerance**     | Requires nodes to survive failures                                            |
| **Safety vs. Liveness** | Strictly guarantees Safety (No data corruption) over Liveness                 |

---

## 5. Deployment & Usage

### Integration

The core Paxos roles can be integrated to resolve state conflicts in a distributed environment:

```python
from core.paxos import Acceptor, Proposer

# 1. Initialize a 3-node cluster (Quorum required: 2)
acceptors = [Acceptor(node_id=1), Acceptor(node_id=2), Acceptor(node_id=3)]

# 2. A client attempts to write data to the cluster
proposer = Proposer(proposer_id=100, acceptors=acceptors)
data_payload = "TRANSACTION_APPROVED_USER_A"

# 3. Execute the Two-Phase Consensus Protocol
success, final_value = proposer.run_consensus(value=data_payload)

if success:
    print(f"Cluster Consensus Reached: {final_value}")
else:
    print("Consensus Failed. Transaction aborted to protect data integrity.")

```

### Running the Simulator

To observe the algorithm resolving dueling requests amidst simulated network packet loss:

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

- **Cloud Infrastructure:** Paxos (and its derivatives like Raft) forms the consensus backbone for coordination services like Apache ZooKeeper and HashiCorp Consul, ensuring critical configuration data is consistent across datacenters.
- **Global Distributed Databases:** Powers the underlying replication logs for massively scalable, globally distributed databases like Google Spanner, allowing them to offer strict ACID guarantees.
- **High-Availability E-Commerce Backends:** Used to elect a "Leader" node in a cluster, ensuring that high-stakes services (like inventory management or payment processing ledgers) remain highly available and perfectly synchronized even during infrastructure outages.
