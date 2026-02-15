# Complexity Analysis: Bloom Filter

A Bloom Filter is a space-efficient probabilistic data structure. Its performance is unique because its time complexity is independent of the number of items stored in the filter, and its space complexity is fixed based on the desired false positive rate.

## 1. Time Complexity

The time complexity for both operations (**Add** and **Check**) is:


### 1.1 Parameter Breakdown

* **:** The number of hash functions used.
* **Note:** Unlike a Hash Map or a Tree, the time taken to check for an item's existence does not increase as you add more items to the set. Whether the filter contains 10 items or 10 million, the time remains constant at  hash calculations.

---

## 2. Space Complexity

The space complexity is:


### 2.1 Parameter Breakdown

* **:** The number of bits in the bit array.
* **Memory Efficiency:** Bloom Filters do not store the actual data items; they only store bits. This allows them to represent a set of 1 million items in just a few megabytes, whereas a standard Hash Set would require gigabytes of RAM to store the actual strings or objects.

---

## 3. The False Positive Probability

The defining characteristic of a Bloom Filter is the trade-off between space and accuracy. The probability of a false positive () is calculated as:


### 3.1 Key Variables

* **:** The number of items currently in the filter.
* **:** The size of the bit array.
* **:** The number of hash functions.

As  (the number of items) increases, the probability of a false positive also increases. Once the bit array becomes too "crowded" (saturated with 1s), the filter becomes less reliable.

---

## 4. Engineering Trade-offs

| Feature | Bloom Filter | Hash Set / Hash Map |
| --- | --- | --- |
| **Membership Test** | Probabilistic (False Positives) | Deterministic (100% Accurate) |
| **Deletions** | Not Supported | Supported |
| **Space Usage** | Extremely Low (Fixed) | High (Grows with ) |
| **Search Speed** | Constant  | Average , Worst  |

---

## 5. Performance Metrics Table

| Metric | Complexity |
| --- | --- |
| **Insertion Time** |  |
| **Search Time** |  |
| **Space Complexity** |  |
| **Deletion Time** | N/A (Impossible in standard Bloom Filter) |