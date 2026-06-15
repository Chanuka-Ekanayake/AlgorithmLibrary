# AES Logic & Mathematical Foundation

The **Advanced Encryption Standard (AES)** is a symmetric block cipher standardized by NIST in 2001 (FIPS-197). It processes data in fixed-size blocks of 128 bits (16 bytes) and supports key lengths of 128, 192, or 256 bits. 

AES operates on a $4 \times 4$ column-major matrix of bytes termed the **State**.

---

## 1. The State Representation

A 16-byte block $B = [b_0, b_1, b_2, \dots, b_{15}]$ is mapped to the State matrix $S$ as follows:
\[
S = \begin{bmatrix}
b_0 & b_4 & b_8 & b_{12} \\
b_1 & b_5 & b_9 & b_{13} \\
b_2 & b_6 & b_{10} & b_{14} \\
b_3 & b_7 & b_{11} & b_{15}
\end{bmatrix}
\]

---

## 2. Core Transformations

Each round of AES (except the final round) consists of four algebraic transformations applied to the State.

### 2.1 SubBytes
A non-linear byte substitution where each byte in the state is replaced by its entry in a static lookup table (the **S-Box**).
- **Mathematical Construction**: The S-Box is constructed by taking the multiplicative inverse of a byte in the finite field $\text{GF}(2^8)$ modulo the irreducible polynomial $x^8 + x^4 + x^3 + x + 1$ (value `0x11b`), followed by an affine transformation over $\text{GF}(2)$.
- **Decryption**: Uses the **Inverse S-Box** (`INV_S_BOX`) to reverse the mapping.

### 2.2 ShiftRows
A linear transposition step where the rows of the state are cyclically shifted to the left by varying offsets:
- Row 0: No shift
- Row 1: Shifted left by 1 byte
- Row 2: Shifted left by 2 bytes
- Row 3: Shifted left by 3 bytes

\[
\begin{bmatrix}
s_{0,0} & s_{0,1} & s_{0,2} & s_{0,3} \\
s_{1,0} & s_{1,1} & s_{1,2} & s_{1,3} \\
s_{2,0} & s_{2,1} & s_{2,2} & s_{2,3} \\
s_{3,0} & s_{3,1} & s_{3,2} & s_{3,3}
\end{bmatrix}
\xrightarrow{\text{ShiftRows}}
\begin{bmatrix}
s_{0,0} & s_{0,1} & s_{0,2} & s_{0,3} \\
s_{1,1} & s_{1,2} & s_{1,3} & s_{1,0} \\
s_{2,2} & s_{2,3} & s_{2,0} & s_{2,1} \\
s_{3,3} & s_{3,0} & s_{3,1} & s_{3,2}
\end{bmatrix}
\]
- **Decryption**: `InvShiftRows` shifts the rows to the right by the same offsets.

### 2.3 MixColumns
An operation that treats each column of the State as a four-term polynomial over $\text{GF}(2^8)$ and multiplies it modulo $x^4 + 1$ with a fixed polynomial $a(x) = \{03\}x^3 + \{01\}x^2 + \{01\}x + \{02\}$.

This is equivalent to matrix multiplication in $\text{GF}(2^8)$:
\[
\begin{bmatrix}
s'_{0,c} \\
s'_{1,c} \\
s'_{2,c} \\
s'_{3,c}
\end{bmatrix}
=
\begin{bmatrix}
02 & 03 & 01 & 01 \\
01 & 02 & 03 & 01 \\
01 & 01 & 02 & 03 \\
03 & 01 & 01 & 02
\end{bmatrix}
\begin{bmatrix}
s_{0,c} \\
s_{1,c} \\
s_{2,c} \\
s_{3,c}
\end{bmatrix}
\]

- **Decryption**: `InvMixColumns` multiplies each column by the inverse matrix:
\[
\begin{bmatrix}
0e & 0b & 0d & 09 \\
09 & 0e & 0b & 0d \\
0d & 09 & 0e & 0b \\
0b & 0d & 09 & 0e
\end{bmatrix}
\]

### 2.4 AddRoundKey
A simple bitwise XOR operation between the State and the corresponding Round Key:
\[
S'_{c} = S_{c} \oplus W_{r, c}
\]
Where $W_{r, c}$ is the word representing column $c$ of the round key for round $r$.

---

## 3. Key Expansion

AES takes the master key and expands it into $N_r + 1$ round keys (128 bits each) using a recursive word-based schedule.
The expansion uses three functions on 4-byte words:
1. **RotWord**: Cyclically shifts a word left by 1 byte: $[b_0, b_1, b_2, b_3] \to [b_1, b_2, b_3, b_0]$.
2. **SubWord**: Replaces each byte in a word with its S-Box value: $[b_0, b_1, b_2, b_3] \to [S(b_0), S(b_1), S(b_2), S(b_3)]$.
3. **Rcon**: XORs the first byte of a word with a round-dependent constant $RC[j]$ derived from powers of 2 in $\text{GF}(2^8)$.

### Key Expansion Logic
For a key of length $N_k$ words:
- The first $N_k$ words of the expanded key are the master key.
- For subsequent words $w_i$:
  - If $i \pmod{N_k} == 0$, then $w_i = w_{i-N_k} \oplus \text{SubWord}(\text{RotWord}(w_{i-1})) \oplus \text{Rcon}[i / N_k]$.
  - Else if $N_k > 6$ (AES-256) and $i \pmod{N_k} == 4$, then $w_i = w_{i-N_k} \oplus \text{SubWord}(w_{i-1})$.
  - Else, $w_i = w_{i-N_k} \oplus w_{i-1}$.

---

## 4. Modes of Operation & Padding

Because AES is a block cipher, messages must be multiples of the 16-byte block size.

### 4.1 PKCS#7 Padding
Fills out the final block to 16 bytes by appending $N$ bytes, each of value $N$ (where $1 \le N \le 16$). If the plaintext is already a multiple of 16, a full block of 16 bytes (each of value `0x10`) is appended so that unpadding is always unambiguous.

### 4.2 ECB Mode (Electronic Codebook)
Each block is encrypted independently.
- **Formula**: $C_i = \text{Encrypt}(P_i, K)$
- **Vulnerability**: Identical plaintext blocks produce identical ciphertext blocks, leaking structural patterns of the plaintext.

### 4.3 CBC Mode (Cipher Block Chaining)
Each plaintext block is XORed with the previous ciphertext block before encryption.
- **Formula (Encrypt)**: $C_i = \text{Encrypt}(P_i \oplus C_{i-1}, K)$, where $C_{-1} = \text{IV}$ (Initialization Vector).
- **Formula (Decrypt)**: $P_i = \text{Decrypt}(C_i, K) \oplus C_{i-1}$
- **Security**: The IV randomizes the encryption process, ensuring identical plaintexts encrypt to entirely different ciphertexts.
