# Consistent Hashing Balancer

## 1. Overview

The **Consistent Hashing Balancer** is a specialized distributed systems module designed to solve the problem of horizontal scaling. In traditional load balancing, adding or removing a server typically requires re-mapping nearly all data (), leading to massive cache misses and system instability.

Consistent Hashing solves this by utilizing a **Circular Hash Ring**, ensuring that when a server enters or leaves the cluster, only a minimal fraction () of the total data needs to be redistributed.

---

## 2. Technical Features

* **Virtual Nodes (VNodes):** Each physical server is mapped to multiple points (default 100) on the ring. This eliminates "hotspots" and ensures an even distribution of traffic across the cluster.
* **Elastic Scaling:** Optimized for cloud-native environments where servers are frequently added (scaling up) or removed (scaling down).
* **High-Speed Routing:** Utilizes **Binary Search** (`bisect`) to find the appropriate server for any given request in **** time.
* **Fault Tolerance:** In the event of a server failure, the ring naturally "heals" by automatically routing requests to the next available neighbor on the ring without requiring a global re-index.

---

## 3. Architecture

```text
.
├── core/                  # Engine Logic
│   ├── __init__.py        # Package initialization
│   └── hash_ring.py       # Ring logic and virtual node management
├── docs/                  # Technical Documentation
│   ├── logic.md           # The "Clockwise Search" and ring wrapping
│   └── complexity.md      # Analysis of data movement vs. modulo hashing
├── test-project/          # Global Load Balancer
│   ├── app.py             # Cluster simulation with scale/fail scenarios
│   └── instructions.md    # Guide for running the distribution audit
└── README.md              # Documentation Entry Point

```

---

## 4. Performance Specifications

| Metric | Specification |
| --- | --- |
| **Lookup Complexity** |  |
| **Data Migration** |  of total keys (Minimal) |
| **Memory Footprint** |  |
| **Scaling Property** | High Elasticity |

---

## 5. Deployment & Usage

### Integration

The `ConsistentHashRing` is designed to be the "brain" of your load balancer or distributed cache:

```python
from core.hash_ring import ConsistentHashRing

# Initialize with your server pool
servers = ["192.168.1.1", "192.168.1.2", "192.168.1.3"]
ring = ConsistentHashRing(nodes=servers, virtual_nodes=100)

# Route a request to the correct server
target_server = ring.get_node("user_session_9982")

```

### Running the Simulator

To observe how the ring handles a server "crash" and redistributes load:

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

* **Distributed Caching:** Used by **Memcached** and **Redis Cluster** to spread keys across multiple instances.
* **Database Partitioning:** The core mechanism behind **Amazon DynamoDB**, **Apache Cassandra**, and **Riak**.
* **Content Delivery Networks (CDNs):** Directing users to the nearest edge server while maintaining cache hits.
* **Microservices:** Balancing stateful requests across an elastic fleet of service instances.