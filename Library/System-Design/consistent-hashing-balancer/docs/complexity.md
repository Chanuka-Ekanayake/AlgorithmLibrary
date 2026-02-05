# Complexity Analysis: Consistent Hashing Balancer

Consistent Hashing is designed for **distributed systems** where nodes (servers) frequently join or leave the cluster. Its primary advantage is minimizing data movement during these transitions.

## 1. Time Complexity

| Operation | Complexity | Description |
| --- | --- | --- |
| **`get_node()` (Lookup)** |  | Finding a node involves a binary search (`bisect_left`) on the sorted list of virtual node hashes. |
| **`add_node()`** |  | Adding a node requires inserting  virtual hashes into the sorted list. Each insertion is logarithmic. |
| **`remove_node()`** |  | Removing a node requires finding and deleting  hashes. In Python lists, deletion is  where  is the total virtual nodes. |

* ****: Number of physical nodes (servers).
* ****: Number of virtual nodes per physical node.

---

## 2. Space Complexity

The space complexity is:


### 2.1 Memory Footprint

* We store two main structures:
1. **A List of Hashes:**  integers.
2. **A Hash Map:**  mappings from hash to physical node name.


* **Scaling Example:** 100 servers with 100 virtual nodes each results in 10,000 entries. This consumes only a few megabytes of RAM, allowing the balancer to run on very modest hardware while managing massive traffic.

---

## 3. Data Movement Complexity (The "Killer Feature")

The true power of Consistent Hashing is revealed when the cluster size changes.

| Method | Scaling Complexity | Data Movement |
| --- | --- | --- |
| **Modulo Hashing ()** |  | **Total.** Almost every key moves to a new server when  changes. |
| **Consistent Hashing** |  | **Minimal.** Only  of the total keys () move to a new server. |

### 3.1 The  Rule

If you have 10 servers and add an 11th, standard hashing would force nearly **100%** of your cached data to be re-mapped. With Consistent Hashing, only approximately **10%** of the data needs to be moved. This prevents "Cache Stampedes" and keeps the system stable during scaling.

---

## 4. Engineering Trade-offs: Virtual Nodes ()

* **High  (e.g., 200+):** Provides near-perfect load distribution (no "hotspots"), but increases the time for `get_node()` lookups and memory usage.
* **Low  (e.g., 10):** Very fast lookups and low memory usage, but can lead to "skewed distribution" where one server handles significantly more traffic than others.
* **Industry Standard:** Most systems (like Dynamo or Cassandra) use between **100 and 200** virtual nodes to balance performance and fairness.

---

## 5. Summary

| Metric | Performance |
| --- | --- |
| **Routing Efficiency** | Logarithmic (O(log V)) |
| **Scaling Stability** | High (O(1/N) movement) |
| **Load Balancing** | Adjustable via Virtual Nodes |