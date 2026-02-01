# Complexity Analysis: LRU Cache

The LRU (Least Recently Used) Cache is designed for high-performance systems where data retrieval speed is the primary bottleneck. By combining a **Hash Map** with a **Doubly Linked List**, we eliminate the need for linear searching.

## 1. Time Complexity

| Operation | Complexity | Description |
| --- | --- | --- |
| **`get(key)`** |  | Instant lookup via Hash Map and  pointer update to move node to front. |
| **`put(key, val)`** |  | Instant insertion into Hash Map and  pointer update to add to front. |
| **`evict()`** |  | The LRU item is always at the `tail.prev`, allowing instant removal. |

### 1.1 Why is it ?

* **The Hash Map Advantage:** Without a map, finding a key would take  time. The map gives us the exact memory address of the node in the linked list instantly.
* **The Linked List Advantage:** In a standard array, moving an item to the front or removing an item from the middle requires shifting all other elements (). In a **Doubly Linked List**, we only need to update the `next` and `prev` pointers of the surrounding nodes, which is a constant-time operation.

---

## 2. Space Complexity

The space complexity is:



Where **** is the defined **Capacity** of the cache.

### 2.1 Memory Usage Breakdown

* **Hash Map Storage:** Stores up to  keys and their corresponding node references.
* **Doubly Linked List:** Stores  nodes, each containing a key, a value, and two pointers.
* **Total footprint:** Proportional to the number of items we allow the cache to hold.

---

## 3. Comparison: Cache Strategies

| Strategy | Lookup | Eviction | Best Use Case |
| --- | --- | --- | --- |
| **LRU (Ours)** |  |  | General purpose; handles "temporal locality" best. |
| **LFU (Least Freq Used)** |  |  | Frequency-based access patterns. |
| **FIFO (First In First Out)** |  |  | Simple queues where age is the only factor. |

---

## 4. Performance Metrics Table

| Metric | Performance |
| --- | --- |
| **Worst-Case Access** |  |
| **Worst-Case Update** |  |
| **Auxiliary Space** |  |
| **Search Paradigm** | Hash-indexed Linked List |

---

## 5. Engineering Trade-offs

* **Memory Overhead:** Because we store both a map and a linked list, we use roughly twice the memory of a simple dictionary. This is the classic "Space-Time Trade-off"—we sacrifice a bit of RAM to gain incredible speed.
* **Thread Safety:** This specific implementation is not thread-safe. In a production 2026 environment (like a multi-threaded web server), you would need to add **Mutex Locks** or use concurrent data structures to prevent race conditions during pointer updates.