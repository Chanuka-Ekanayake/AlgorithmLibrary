# Complexity Analysis: Fenwick Tree (BIT)

A Binary Indexed Tree abandons the idea of updating every single index that comes after a modified value. Instead, it delegates responsibility for specific ranges of data to specific indices based entirely on their binary representation.

## 1. Time Complexity

Let be the total size of the array (e.g., the number of days in your sales history).

| Operation        | Complexity  | Explanation                                                                                                                   |
| ---------------- | ----------- | ----------------------------------------------------------------------------------------------------------------------------- |
| **Point Update** | O(log n)    | Adding a value to a specific index. The algorithm only touches the nodes that strictly "cover" this index, skipping the rest. |
| **Prefix Query** | O(log n)    | Summing from index 1 to . The algorithm jumps backward, collecting pre-calculated sub-sums, instead of iterating one by one.  |
| **Range Query**  | O(log n)    | Summing from index to . This is just two prefix queries executed back-to-back: `Query(R) - Query(L-1)`.                       |
| **Naive Build**  | O(n log n)  | Inserting items into an empty tree one by one.                                                                                |
| **Linear Build** | O(n)        | Constructing the tree in a single pass by explicitly adding each node's value to its direct mathematical parent.              |

### The Bounds Explained

The time complexity of a Fenwick Tree query or update is strictly bound by the number of set bits (1s) in the binary representation of the index .

If you have an array of 1,000,000 elements, in a standard loop, querying the sum up to the end takes 1,000,000 operations.
In a Fenwick Tree, the number 1,000,000 in binary is `11110100001001000000` (which has 7 set bits). To calculate the sum of the first 1,000,000 elements, the Fenwick Tree executes exactly **7 addition operations**. Even in the absolute worst-case scenario, the maximum number of operations for a 1,000,000-element tree is about 20.

---

## 2. Space Complexity

The Fenwick Tree is legendary for its incredibly minimal memory footprint.

| Structure              | Space Required | Description                                                                        |
| ---------------------- | -------------- | ---------------------------------------------------------------------------------- |
| **Tree Array**         |                | The tree is stored as a flat, 1-dimensional array of size (index 0 is left empty). |
| **Auxiliary Overhead** |                | No node objects, no left/right pointers, and no recursion stacks are used.         |

### Fenwick Tree vs. Segment Tree

A Segment Tree can do everything a Fenwick Tree can do, plus more (like finding the minimum/maximum in a range). However, a Segment Tree requires allocating an array of size to represent the full binary tree structure.

If you are building a real-time revenue dashboard that tracks 10,000,000 individual user accounts, a Segment Tree forces you to allocate memory for 40,000,000 nodes. A Fenwick Tree requires exactly 10,000,001 indices. When memory and cache-locality matter, the Fenwick Tree wins flawlessly.
