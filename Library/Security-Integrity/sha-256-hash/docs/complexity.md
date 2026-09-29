# Complexity Analysis: SHA-256

## 1. Time Complexity

The time complexity of hashing a message using SHA-256 is strictly linear with respect to the length of the input message:

**Time Complexity: $\mathcal{O}(L)$** (where $L$ is the length of the message in bits)

### Breakdown per Block
SHA-256 processes the message in 512-bit blocks. For every single block, the algorithm executes exactly the same operations:
1. Message Schedule Extension (16 words $\rightarrow$ 64 words): 48 iterations of bitwise operations.
2. Compression Loop: 64 iterations of complex bitwise logic (Ch, Maj, Rotations, Additions).
3. Hash State Addition: 8 integer additions.

Because the work done per 512-bit block is a fixed constant, the total time required is $C \times \lceil \frac{L}{512} \rceil$, which simplifies asymptotically to $\mathcal{O}(L)$.

---

## 2. Space Complexity

The space complexity is exceptionally low. 

**Space Complexity: $\mathcal{O}(1)$** (Auxiliary space, excluding the storage of the input message itself)

### Breakdown
During execution, the algorithm only ever needs to hold:
1. The 64 constants ($K$ array)
2. The 8 running state variables ($a \dots h$)
3. The current 512-bit chunk being processed.
4. The 64-word message schedule array ($W$) for the current chunk.

Because blocks are processed sequentially, the memory required never grows, regardless of whether you are hashing a 1 KB text file or a 50 GB database dump. You only ever need enough RAM to hold one 512-bit block at a time (this is called *streaming* a hash).

---

## 3. Cryptographic Complexities (Security Limits)

In cryptography, we also measure the time complexity of "breaking" the algorithm:

### 3.1 Pre-image Attack (Reversing the Hash)
Given a specific hash $H$, find a message $M$ such that $SHA256(M) = H$.
Because the algorithm is a one-way function, the only way to find $M$ is a brute-force search over the 256-bit output space.
**Time Complexity:** $\mathcal{O}(2^{256})$ operations. (Functionally impossible. $2^{256}$ is roughly the number of atoms in the visible universe).

### 3.2 Collision Attack (Finding duplicates)
Find *any* two different messages $M_1$ and $M_2$ such that $SHA256(M_1) = SHA256(M_2)$.
Because of the **Birthday Paradox** in probability, the time complexity to find a collision is the square root of the total output space.
**Time Complexity:** $\mathcal{O}(2^{128})$ operations. (Still computationally infeasible with modern technology, requiring millions of years on supercomputers).

## 4. Optimization in Practice
While this package provides a pure Python implementation for educational clarity, real-world hashing (like in the `hashlib` standard library or Bitcoin ASIC miners) is heavily optimized:
- Written in C or hardware-level logic gates.
- Uses CPU extensions specifically designed to execute SHA-256 rounds natively (e.g., Intel SHA Extensions).
