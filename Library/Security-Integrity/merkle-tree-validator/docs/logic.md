# Algorithm Logic: Merkle Tree (Hash Tree)

## 1. The Core Principle: "Trust from the Ground Up"

A Merkle Tree is a binary tree where every leaf node is the hash of a data block, and every non-leaf node is the hash of its children's combined hashes.

In your software marketplace, if you are selling a **10GB Machine Learning Model**, you cannot simply give the user one hash for the whole file. If the download fails at 9.9GB, the user has to restart. By using a Merkle Tree, we break the model into small chunks (e.g., 1MB each). The user can verify each chunk as it arrives.

---

## 2. The Build Process

Our implementation follows these logical steps:

1. **Chunking:** The input data is split into fixed-size blocks (chunks).
2. **Leaf Hashing:** Each block is passed through **SHA-256**. These become the "leaves" (Level 0).
3. **Pairing:** We take two adjacent hashes and concatenate them: `H(A) + H(B)`.
4. **Parent Hashing:** We hash the concatenated string to create a parent node: `H(AB) = SHA256(H(A) + H(B))`.
5. **Recursion:** We repeat this process upward until only one hash remains. This is the **Merkle Root**.

### Handling "Odd" Numbers

If a level has an odd number of nodes, the algorithm cannot find a pair for the last node. Our implementation solves this by **duplicating the last node** to create a pair, ensuring the tree remains a complete binary structure.

---

## 3. The "Merkle Proof" (The Magic of Log n)

The most powerful part of the logic is the **Proof**. If a user wants to verify that "Block 3" is correct, they don't need the whole tree. They only need the **Path of Siblings**.

To verify Block 3 (index 2), the user needs:

1. **The Hash of Block 3.**
2. **The Sibling of Block 3** (Block 4's hash).
3. **The Sibling of their Parent** (the hash representing Blocks 1 & 2).

By "climbing" the tree with these few hashes, they can recalculate the Root. If their calculated Root matches the trusted Root provided by the marketplace, the data is **100% authentic**.

---

## 4. Logic Flow: Verification

When `verify_proof()` is called:

1. **Start** with the hash of the data you want to check.
2. **Iterate** through the "Proof" list (the siblings).
3. **Rehash:** Combine the current hash with the sibling hash from the proof. (Order matters: is the sibling to the `left` or `right`?)
4. **Compare:** Once you reach the top, check if your result equals the `root_hash`.

---

## 5. Why SHA-256?

We use SHA-256 because it is **Collision-Resistant**. It is mathematically impossible (within current computational limits) to find two different data blocks that produce the same hash. This ensures that a malicious actor cannot swap a "clean" software binary with a "malware" version without changing the Merkle Root.