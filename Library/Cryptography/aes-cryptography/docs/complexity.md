# Complexity Analysis: AES

As a block cipher, the primary algorithmic unit of AES operates on a fixed-size block of 16 bytes (128 bits). Consequently, all core operations on a single block run in constant time and space.

---

## 1. Single-Block Operations Complexity

For a single 16-byte block, the complexity breakdown is:

| Operation | Time Complexity | Space Complexity | Description |
| --- | --- | --- | --- |
| **SubBytes / InvSubBytes** | $O(1)$ | $O(1)$ | 16 lookup table checks. |
| **ShiftRows / InvShiftRows** | $O(1)$ | $O(1)$ | In-place cyclic byte rearrangements. |
| **MixColumns / InvMixColumns** | $O(1)$ | $O(1)$ | Standard matrix multiplications in finite field $\text{GF}(2^8)$ (16 linear combinations). |
| **AddRoundKey** | $O(1)$ | $O(1)$ | 16 bitwise XOR operations. |
| **Total Block Encryption** | $O(1)$ | $O(1)$ | Performs $N_r$ rounds of the above steps (where $N_r \in \{10, 12, 14\}$). |

---

## 2. Key Expansion Complexity

Before processing the message, the master key is expanded into a schedule of round keys.

| Key Size | Master Key Length | Rounds ($N_r$) | Words in Schedule | Time Complexity | Space Complexity |
| --- | --- | --- | --- | --- | --- |
| **128-bit** | 16 bytes | 10 | 44 | $O(1)$ | $O(1)$ |
| **192-bit** | 24 bytes | 12 | 52 | $O(1)$ | $O(1)$ |
| **256-bit** | 32 bytes | 14 | 60 | $O(1)$ | $O(1)$ |

- **Time Complexity**: $O(N_r)$ which is $O(1)$ because the number of rounds is capped at 14.
- **Space Complexity**: $O(N_r)$ which is $O(1)$ to store the expanded round keys (maximum 240 bytes).

---

## 3. Full Message Encryption & Decryption Complexity

For a message containing $N$ bytes of data:

- **Time Complexity**: $O(N)$
  - The message is padded to a multiple of 16 bytes.
  - The number of blocks is $M = \lceil (N + 1) / 16 \rceil$.
  - Each block is processed in $O(1)$ time. Thus, the total time to encrypt or decrypt $M$ blocks is $O(M) = O(N)$.
  
- **Space Complexity**: $O(N)$
  - Storing the output plaintext or ciphertext requires $O(N)$ space.
  - The auxiliary space used during processing (the State matrix) is only $O(1)$ (16 bytes).

---

## 4. Engineering Trade-offs

### 4.1 Lookup Tables vs. On-The-Fly Computation
- **This Implementation**: We use precomputed tables for `S_BOX` and `INV_S_BOX` to achieve $O(1)$ time complexity for byte substitution. Galois Field multiplication by constants is computed using bitwise operations (`gmul_2`, etc.) which avoids large product tables while remaining fast and readable.
- **Hardware Implementations**: High-performance production systems often use dedicated CPU instructions (like Intel's `AES-NI`) to perform these operations in hardware, which mitigates software side-channel vulnerabilities (like cache-timing attacks).
