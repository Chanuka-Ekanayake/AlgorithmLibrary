# Complexity Analysis: ElGamal Cryptosystem

ElGamal's efficiency is rooted in the speed of **Modular Exponentiation**, while its security is rooted in the computational "hardness" of the **Discrete Logarithm Problem (DLP)**.

## 1. Time Complexity

| Operation          | Complexity | Description                                                     |
| ------------------ | ---------- | --------------------------------------------------------------- |
| **Key Generation** |            | Requires one modular exponentiation to compute .                |
| **Encryption**     |            | Requires two modular exponentiations (to compute and ).         |
| **Decryption**     |            | Requires one modular exponentiation () and one modular inverse. |

### The Binary Exponentiation Advantage

Our implementation uses Python's `pow(base, exp, mod)`, which utilizes **Exponentiation by Squaring**. This reduces the number of multiplications from (linear) to (logarithmic). For a 2048-bit prime, this means only ~2048 multiplications instead of operations.

---

## 2. Space Complexity

| Component       | Complexity | Description                                                     |
| --------------- | ---------- | --------------------------------------------------------------- |
| **Public Key**  |            | Stores three large integers .                                   |
| **Private Key** |            | Stores one large integer .                                      |
| **Ciphertext**  |            | ElGamal doubles the message size, as the ciphertext is a pair . |

---

## 3. Security vs. Complexity (The DLP)

The complexity of **breaking** ElGamal is what provides its value. An attacker given must find such that:

- **Classical Complexity:** The best-known classical algorithm (General Number Field Sieve) runs in sub-exponential time, but is still computationally infeasible for primes above 2048 bits.
- **Quantum Complexity:** Using **Shor’s Algorithm**, a quantum computer could solve this in time, which is why post-quantum research is a major focus in 2026.

---

## 4. Engineering Trade-offs

- **Message Expansion:** Unlike RSA, ElGamal ciphertexts are twice as long as the plaintext. This makes it less space-efficient for very large files, but ideal for encrypting symmetric keys (like AES keys).
- **Randomization Cost:** Every encryption requires a new random ephemeral key . Generating high-quality entropy (randomness) adds a slight overhead to the encryption process compared to deterministic algorithms.
- **Prime Selection:** The security depends on having at least one large prime factor. Using a "Safe Prime" () is standard practice to prevent specific mathematical shortcuts.
