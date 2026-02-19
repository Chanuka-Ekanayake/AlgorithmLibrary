# Complexity Analysis: ElGamal Cryptosystem

ElGamal's efficiency is rooted in the speed of **Modular Exponentiation**, while its security is rooted in the computational "hardness" of the **Discrete Logarithm Problem (DLP)**.

## 1. Time Complexity

| Operation          | Complexity        | Description                                                                                   |
| ------------------ | ----------------- | --------------------------------------------------------------------------------------------- |
| **Key Generation** | \(O(\log p)\)     | Requires one modular exponentiation to compute the public component \(y = g^x \bmod p\).      |
| **Encryption**     | \(O(\log p)\)     | Requires two modular exponentiations (to compute \(c_1 = g^k \bmod p\) and \(c_2 = m y^k\bmod p\)). |
| **Decryption**     | \(O(\log p)\)     | Requires one modular exponentiation (to compute \(s = c_1^x \bmod p\)) and one modular inverse to recover \(m = c_2 s^{-1} \bmod p\). |

### The Binary Exponentiation Advantage

Our implementation uses Python's `pow(base, exp, mod)`, which utilizes **Exponentiation by Squaring**. This reduces the number of multiplications from linear \(O(n)\) to logarithmic \(O(\log n)\). For a 2048-bit prime, this means only ~2048 multiplications instead of ~\(2^{2048}\) operations.

---

## 2. Space Complexity

| Component       | Complexity        | Description                                                                 |
| --------------- | ----------------- | --------------------------------------------------------------------------- |
| **Public Key**  | \(O(\log p)\)     | Stores three large integers \((p, g, y)\).                                  |
| **Private Key** | \(O(\log p)\)     | Stores one large integer \(x\).                                             |
| **Ciphertext**  | \(O(\log p)\)     | ElGamal doubles the message size, as the ciphertext is a pair \((c_1, c_2)\). |

---

## 3. Security vs. Complexity (The DLP)

The complexity of **breaking** ElGamal is what provides its value. An attacker given \((p, g, y = g^x \bmod p)\) must find \(x\) such that \(y = g^x \bmod p\):

- **Classical Complexity:** The best-known classical algorithm (General Number Field Sieve) runs in sub-exponential time, but is still computationally infeasible for primes above 2048 bits.
- **Quantum Complexity:** Using **Shor’s Algorithm**, a quantum computer could solve this in polynomial time, which is why post-quantum research is a major focus in 2026.

---

## 4. Engineering Trade-offs

- **Message Expansion:** Unlike RSA, ElGamal ciphertexts are twice as long as the plaintext. This makes it less space-efficient for very large files, but ideal for encrypting symmetric keys (like AES keys).
- **Randomization Cost:** Every encryption requires a new random ephemeral key \(k\). Generating high-quality entropy (randomness) adds a slight overhead to the encryption process compared to deterministic algorithms.
- **Prime Selection:** The security depends on having at least one large prime factor. Using a "Safe Prime" \(p = 2q + 1\) is standard practice to prevent specific mathematical shortcuts.
