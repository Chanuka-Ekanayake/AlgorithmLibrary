# Complexity Analysis: HyperLogLog (HLL)

HyperLogLog is a probabilistic algorithm used to estimate the number of unique elements (cardinality) in a set. Its primary value proposition is **memory efficiency at the cost of a small, predictable error rate.**

## 1. Time Complexity

| Operation | Complexity | Description |
| --- | --- | --- |
| **`add(item)`** |  | Hashing the item and updating a single register index are constant-time operations. |
| **`count()`** |  | Calculating the harmonic mean requires iterating through all  registers once. |
| **Merge** |  | Two HLL structures can be merged by taking the maximum of each corresponding register. |

### 1.1 Independence of 

Note that the time complexity for `add` is completely independent of the number of unique elements () already in the set. Whether you have 100 or 100,000,000 items, the cost to add a new one remains exactly the same.

---

## 2. Space Complexity

The space complexity of HyperLogLog is:



For all practical purposes in modern computing, this is treated as ** (Constant Space)**.

### 2.1 Memory Footprint

* **Registers ():** The memory usage is determined by the number of registers, which is .
* **Size per Register:** Each register only needs to store the position of the first `1` bit in a hash. For a 64-bit hash, the maximum value is 64, which fits in just **6 bits**.
* **Real-world Example:** With a precision of  ( registers), the error rate is , and the structure occupies roughly **3 KB** of RAM. This same 3 KB can estimate a set of 1,000 items or 1,000,000,000 items.

---

## 3. Accuracy vs. Memory

The standard error for HyperLogLog is calculated as:


| Precision () | Registers () | Approx. Error | Memory Usage |
| --- | --- | --- | --- |
| 10 | 1,024 | 3.25% | ~1 KB |
| 12 | 4,096 | 1.62% | ~3 KB |
| 14 | 16,384 | 0.81% | ~12 KB |
| 16 | 65,536 | 0.40% | ~48 KB |

---

## 4. Comparison with Exact Sets

| Feature | Standard `set` / `HashSet` | HyperLogLog |
| --- | --- | --- |
| **Accuracy** | 100% (Exact) | ~98-99% (Estimated) |
| **Space** |  (Linear) |  (Constant) |
| **1M UUIDs** | ~64 MB RAM | ~3 KB RAM |
| **1B UUIDs** | ~60 GB RAM | ~3 KB RAM |

---

## 5. Engineering Trade-offs

* **The "Small Range" Problem:** HLL is naturally biased when the number of elements is very small (near 0). Our implementation uses **Linear Counting** as a correction mechanism to maintain accuracy for small datasets.
* **Non-Reversibility:** You can count how many unique items are in the set, but you **cannot** retrieve the items themselves. HLL is a summary, not a storage container.