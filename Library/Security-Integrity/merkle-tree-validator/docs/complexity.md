# Complexity Analysis: Merkle Tree (Hash Tree)

The Merkle Tree is the gold standard for **efficient integrity verification**. It allows us to verify a large dataset without requiring the entire dataset to be present during the check.

## 1. Time Complexity

| Operation | Complexity | Description |
| --- | --- | --- |
| **Construction** |  | Every data block must be hashed once, and every pair of hashes is hashed to form the parent. |
| **Root Generation** |  | Inherent in construction; involves  hashes, which converges to . |
| **Proof Generation** |  | Traversing from a leaf to the root takes time proportional to the tree height. |
| **Verification** |  | Reconstructing the root from a leaf hash and its siblings requires only  hashes. |

### 1.1 The Power of Logarithmic Verification

In a dataset with **1,048,576 blocks** ():

* A linear check (hashing everything) requires **1,048,576** operations.
* A Merkle Proof requires only **20** operations.
This  performance is what allows a smartphone to verify a single transaction in a massive blockchain without downloading the whole ledger.

---

## 2. Space Complexity

The space complexity is:



Where **** is the number of data blocks.

### 2.1 Memory Footprint

* **Leaf Nodes:**  hashes.
* **Internal Nodes:** Approximately  hashes to build the tree to the root.
* **Total Storage:**  hashes. Using SHA-256, each hash is 32 bytes (256 bits). For 1,000 blocks, this is roughly **64 KB** of metadata—a negligible footprint for modern systems.

---

## 3. Comparison: Integrity Checks

| Method | Verification | Update Cost | Best Use Case |
| --- | --- | --- | --- |
| **Checksum (MD5/SHA)** |  |  | Small files, single-file downloads. |
| **Merkle Tree (Ours)** |  |  | Large files, P2P sharing, Blockchain. |
| **Bloom Filter** |  |  | Membership testing (Probabilistic). |

---

## 4. Engineering Trade-offs

* **Hashing Overhead:** While verification is , the initial construction requires hashing the entire file. For massive files (e.g., 50GB ML models), this is a one-time  compute-heavy task usually performed by the server.
* **Tree Depth:** If the number of blocks is not a power of 2, the tree can become slightly unbalanced. Our implementation solves this by **padding** (duplicating the last hash), ensuring consistent  depth.

---

## 5. Performance Summary

| Metric | Performance |
| --- | --- |
| **Tree Height** |  |
| **Hashes for Proof** |  |
| **Security Standard** | SHA-256 (Collision Resistant) |
| **Verification Speed** | Extremely High () |