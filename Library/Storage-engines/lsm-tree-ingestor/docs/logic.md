# Algorithm Logic: LSM-Tree MemTable

## 1. The "Write-Fast, Read-Later" Philosophy

In a standard database, every write must update a central index (like a B-Tree), which causes random disk jumps. The **LSM-Tree (Log-Structured Merge-Tree)** flips this. It treats incoming data as a stream.

The **MemTable** is the first stop for all data. Its job is to absorb writes at memory speed and organize them so that when they finally hit the disk, they do so in a perfectly ordered, sequential "burst."

---

## 2. The Lifecycle of a Write

Our implementation follows this logical path:

1. **Ingestion:** Data arrives as a Key-Value pair (e.g., `User_ID: Last_Login_Time`).
2. **Buffering:** The data is stored in a `dict` (in a full system, this would be a **SkipList** or **Self-Balancing Tree** to keep it sorted in real-time).
3. **Threshold Check:** We check if the MemTable has reached its capacity limit (e.g., 100 entries).
4. **The Immutable Switch:** Once full, the MemTable is marked for "Flushing." In a production system, a new MemTable is instantly swapped in so writes are never blocked.

---

## 3. The Flush: Creating an SSTable

The most critical part of the logic is the **Flush** process.

To ensure disk reads are efficient later, we cannot just dump the memory to a file. We must turn the MemTable into an **SSTable (Sorted String Table)**:

* **Sort:** We sort all keys alphabetically.
* **Sequential Write:** We write the sorted data to disk as one continuous block.
* **Immutability:** Once written, an SSTable never changes. To "update" a value, the LSM-Tree simply writes a newer version in a fresh SSTable. The older version is cleaned up later during **Compaction**.

---

## 4. Search Logic: The Layered Approach

When looking for a key (`get`):

1. **Check MemTable:** Is the data in RAM? (Fastest access.).
2. **Check SSTables:** If not in RAM, search the sorted files on disk. Because they are sorted, we can use **Binary Search** or **Bloom Filters** (Algorithm #6) to find the data without reading the whole file.

---

## 5. Why this matters for your Marketplace

If you are logging **Machine Learning Model Telemetry** (e.g., every time an AI model makes a prediction), you are generating thousands of events per second.

* **Traditional DB:** Would choke on the disk seeks.
* **LSM-Tree (MemTable):** Buffers those events in RAM and writes them to the disk in 1MB chunks every few seconds. This reduces disk wear and maximizes throughput.