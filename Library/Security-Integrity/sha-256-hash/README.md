# SHA-256 (Secure Hash Algorithm 256-bit)

## 1. Overview

**SHA-256** is a cryptographic hash function published by the National Institute of Standards and Technology (NIST) as a U.S. Federal Information Processing Standard (FIPS). It belongs to the SHA-2 family of algorithms. 

A cryptographic hash function takes an arbitrary amount of input data and produces a fixed-size (256-bit) string of characters, which typically appears as a 64-character hexadecimal number. It is a **one-way function**; it is computationally infeasible to invert the hash back to its original input.

---

## 2. Technical Features

- **Pure Python Implementation:** Built from scratch using raw bitwise operations (AND, XOR, bit-shifting, right-rotation) to expose the exact mathematical mechanics.
- **Deterministic:** The same input will always produce the exact same 256-bit output.
- **Avalanche Effect:** Changing a single bit of the input completely drastically changes the entire hash output.
- **Collision Resistance:** It is mathematically improbable to find two different inputs that produce the same output hash.
- **Block Processing:** Processes data in 512-bit chunks using a 64-step compression function.

---

## 3. Architecture

```text
.
├── core/                  # Cryptography Engine
│   ├── __init__.py        # Package initialization
│   └── sha256.py          # Pure Python bitwise implementation of SHA-256
├── docs/                  # Technical Documentation
│   ├── logic.md           # The Merkle-Damgård construction, padding, and compression
│   └── complexity.md      # Analysis of time/space scaling and cryptographic limits
├── test-project/          # SHA-256 Simulator
│   ├── app.py             # Demos the avalanche effect and a Proof-of-Work (Bitcoin) miner
│   └── instructions.md    # Guide for running the simulator
└── README.md              # Documentation Entry Point
```

---

## 4. Performance Specifications

| Metric                  | Specification                                   |
| ----------------------- | ----------------------------------------------- |
| **Output Size**         | Exactly 256 bits (64 hexadecimal characters)    |
| **Block Size**          | 512 bits (64 bytes)                             |
| **Time Complexity**     | O(L) where L is the length of the message       |
| **Space Complexity**    | O(1) beyond storing the message                 |
| **Security Limit**      | 128-bit collision resistance (Birthday attack)  |

---

## 5. Deployment & Usage

### Integration

The `sha256` function is simple to use and accepts string or bytes input:

```python
from core.sha256 import sha256

# Hash a string
text = "Hello, world!"
hash_hex = sha256(text)
print(f"Hash: {hash_hex}")
# Output: 315f5bdb76d078c43b8ac0064e4a0164612b1fce77c869345bfc94c75894edd3

# Verify a file or password (deterministic output)
password_guess = "my_secure_password"
if sha256(password_guess) == stored_hash:
    print("Access Granted")
```

### Running the Simulator

To watch the SHA-256 algorithm in action, including a demonstration of the Avalanche Effect and a mini Bitcoin-style Proof-of-Work miner:

1. Navigate to the `test-project` directory:
   ```bash
   cd test-project
   ```
2. Run the simulation:
   ```bash
   python app.py
   ```

---

## 6. Industrial Applications

SHA-256 is the absolute backbone of modern digital security:

- **Cryptocurrencies (Bitcoin):** Used as the Proof-of-Work (PoW) mining algorithm and for generating wallet addresses.
- **Version Control (Git):** Although Git uses SHA-1 by default, many modern systems use SHA-256 for identifying commits and ensuring repository integrity.
- **TLS/SSL Certificates:** Secures web traffic (HTTPS) by verifying the digital signatures of websites.
- **Password Hashing:** Often used (in combination with salts and multiple rounds, or algorithms like PBKDF2) to securely store user passwords in databases.
- **Data Integrity:** Checksums (like `sha256sum`) verify that downloaded files have not been corrupted or tampered with.
