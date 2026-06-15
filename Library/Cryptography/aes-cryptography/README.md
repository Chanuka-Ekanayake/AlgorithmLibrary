# AES (Advanced Encryption Standard) Cryptography

## 1. Overview
The **Advanced Encryption Standard (AES)** is the global standard symmetric-key block cipher. It operates on fixed blocks of 128 bits (16 bytes) of data using key sizes of 128, 192, or 256 bits. 

This module provides a pure Python implementation of AES, including key expansion, Galois Field state transformations, and block cipher modes of operation (ECB and CBC).

---

## 2. Security Notice
> [!WARNING]
> This implementation is for **educational purposes only**. It lacks side-channel hardening (e.g., against cache-timing attacks) and is not intended for production systems. For securing real-world production secrets, always use vetted libraries such as Python's `cryptography` package or hardware-accelerated APIs.

---

## 3. Directory Structure
```text
.
├── core/                  # Pure Python implementation
│   ├── __init__.py        # Exports AES
│   └── aes.py             # Core logic, padding, and block modes
├── docs/                  # Detailed documentation
│   ├── logic.md           # Mathematical and state-transition breakdown
│   └── complexity.md      # Space and time complexity analysis
├── test-project/          # Interactive Application
│   ├── app.py             # CLI Simulator (ECB vs CBC demonstration)
│   └── instructions.md    # Instructions on running the simulator
└── README.md              # Module overview (Current File)
```

---

## 4. Quick Start

### Basic Encryption & Decryption (CBC Mode)

```python
import os
from core.aes import AES

# 1. Instantiate AES with a 256-bit (32-byte) key
key = os.urandom(32)
cipher = AES(key)

# 2. Encrypt using CBC mode (requires a 16-byte IV)
iv = os.urandom(16)
plaintext = b"Confidential system payload."
ciphertext = cipher.encrypt_cbc(plaintext, iv)

# 3. Decrypt using CBC mode
decrypted = cipher.decrypt_cbc(ciphertext, iv)
print(decrypted)  # b"Confidential system payload."
```

---

## 5. Complexity Summary

| Operation | Time Complexity | Space Complexity |
| --- | --- | --- |
| **Key Expansion** | $O(1)$ | $O(1)$ |
| **Block Encryption (16 bytes)** | $O(1)$ | $O(1)$ |
| **Message Processing ($N$ bytes)** | $O(N)$ | $O(N)$ |

For a complete analysis, see [docs/complexity.md](file:///c:/Users/umesh/Desktop/Github%20projects/AlgorithmLibrary/Library/Cryptography/aes-cryptography/docs/complexity.md).

---

*Back to [Main Repository](file:///c:/Users/umesh/Desktop/Github%20projects/AlgorithmLibrary/README.md)*
