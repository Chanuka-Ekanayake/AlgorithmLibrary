# Complexity Analysis: LSM-Tree MemTable

The Log-Structured Merge-Tree (LSM) is designed to handle **extreme write pressure** by deferring disk updates and prioritizing sequential I/O.

## 1. Time Complexity

| Operation | Complexity | Description |
| --- | --- | --- |
| **`put()` (Write)** |  | Data is simply inserted into an in-memory hash map or skip-list. |
| **`get()` (Read)** |  | A point-lookup in the MemTable is near-instantaneous. |
| **`flush()` (Prep)** |  | Sorting the in-memory buffer before writing to disk (the "Merge" step). |
| **Disk Write** |  | **Sequential I/O.** Writing a sorted block to disk is significantly faster than random access. |

### 1.1 The Write-Amplification Trade-off

While writes are  in memory, the system eventually pays a cost during **Compaction** (merging multiple SSTables on disk). However, for the application layer, the perceived latency remains , which is why LSM-trees are preferred for logging, telemetry, and real-time analytics.

---

## 2. Space Complexity

The space complexity is:



Where **** is the **Threshold Capacity** of the MemTable.

### 2.1 Memory Management

* **Memory Bound:** The MemTable occupies a fixed amount of RAM. Once it hits the threshold (e.g., 64MB), it transforms into an immutable state and flushes.
* **Storage Footprint:** The data eventually lives on disk as **SSTables**, which are highly compressible because the data is sorted.

---

## 3. Sequential vs. Random I/O

This is the core "Win" of the LSM-Tree.

| Action | B-Tree (Standard SQL) | LSM-Tree (NoSQL/Ours) |
| --- | --- | --- |
| **Write Pattern** | **Random Writes** (Slow) | **Sequential Writes** (Fast) |
| **Disk Seek** | High (Moving disk heads) | Low (Stream of data) |
| **Throughput** | Limited by Disk Latency | Limited by RAM Speed |

---

## 4. Engineering Trade-offs: The "Read Penalty"

* **The Problem:** If a key isn't in the MemTable, the system must search through multiple SSTable files on disk. This is why reads can be  or worse if not optimized.
* **The Solution:** In your 2026 marketplace, we pair the LSM-Tree with the **Bloom Filter** (which we built as Algorithm #6). The Bloom Filter tells us instantly if a key is *definitely not* on disk, skipping unnecessary I/O.

---

## 5. Performance Summary

| Metric | Performance |
| --- | --- |
| **Write Latency** | Ultra-Low (RAM Speed) |
| **Ingestion Rate** | High (Millions of events/sec) |
| **I/O Efficiency** | High (Sequential Only) |
| **Best Use Case** | Log Aggregation, Time-Series, ML Telemetry |