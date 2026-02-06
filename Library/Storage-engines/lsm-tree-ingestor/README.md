# LSM-Tree Ingestor (MemTable)

## 1. Overview

The **LSM-Tree (Log-Structured Merge-Tree) MemTable** is a write-optimized storage component designed to handle massive data ingestion rates. Traditional databases (B-Trees) often suffer from "Random Write Penalties" because every update requires jumping to different locations on a physical disk.

The LSM-Tree architecture solves this by treating all writes as a high-speed sequential stream. The **MemTable** acts as the initial in-memory buffer that captures these writes at RAM speed, organizes them, and flushes them to disk as ordered, immutable blocks called **SSTables (Sorted String Tables)**.

---

## 2. Technical Features

* **Write-Back Architecture:** All incoming `put` operations are handled in memory with **** complexity, shielding the application from disk latency.
* **Sequential I/O Optimization:** By sorting data in memory before flushing, the engine ensures the disk only performs sequential writes—the fastest possible operation for both SSDs and HDDs.
* **Immutable SSTable Generation:** Once a threshold is reached, the MemTable is "frozen" and written to disk. These files are never modified, which simplifies concurrency and recovery.
* **Tombstone Support:** Deletions are handled as "Tombstone" writes, allowing the system to maintain high write speeds even for delete-heavy workloads.

---

## 3. Architecture

```text
.
├── core/                  # Storage Engine Components
│   ├── __init__.py        # Package initialization
│   └── memtable.py        # In-memory buffer & sorting logic
├── docs/                  # Technical Documentation
│   ├── logic.md           # The Write-Ahead philosophy and flushing math
│   └── complexity.md      # Sequential vs. Random I/O analysis
├── test-project/          # High-Throughput Telemetry Logger
│   ├── app.py             # Simulator for burst-logging ML model events
│   └── instructions.md    # Guide for auditing SSTable flushes
└── README.md              # Documentation Entry Point

```

---

## 4. Performance Specifications

| Metric | Specification |
| --- | --- |
| **Write Throughput** | Ultra-High ( RAM Speed) |
| **Read Latency (RAM)** |  (Direct Access) |
| **Read Latency (Disk)** |  (via Sorted SSTables) |
| **I/O Strategy** | Append-Only / Sequential |

---

## 5. Deployment & Usage

### Integration

The `MemTable` is the primary interface for any write-heavy logging or storage service:

```python
from core.memtable import MemTable

# Initialize with a 64MB-equivalent threshold (e.g., 10,000 entries)
ingestor = MemTable(threshold_size=10000)

# Rapidly ingest telemetry data
def log_event(event_id, data):
    if ingestor.put(event_id, data):
        # Threshold reached! Trigger a flush to persistent storage
        sorted_block = ingestor.flush()
        save_to_sstable(sorted_block)

```

### Running the Simulator

To observe the MemTable filling up and triggering a "Sorted Flush" to a simulated disk:

1. Navigate to the `test-project` directory:
```bash
cd test-project

```


2. Run the telemetry logger:
```bash
python app.py

```



---

## 6. Industrial Applications

* **High-Scale Databases:** The core engine behind **RocksDB**, **LevelDB**, **Apache Cassandra**, and **Google BigTable**.
* **Log Aggregation:** Handling millions of log lines per second in systems like **ELK Stack** or **Splunk**.
* **Time-Series Data:** Storing sensor data or financial ticks where write speed is the primary bottleneck.
* **ML Model Monitoring:** Capturing real-time inference telemetry across distributed AI clusters.