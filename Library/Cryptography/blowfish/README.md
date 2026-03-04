# Blowfish (Symmetric-Key Block Cipher)

## 1. Overview

When operating an e-commerce platform that distributes proprietary Machine Learning models and premium software binaries, securing the transport layer (HTTPS) is not enough. The digital assets and their corresponding license keys must be mathematically encrypted before transmission to prevent interception, spoofing, and unauthorized access.

**Blowfish** is a highly influential symmetric-key block cipher designed by Bruce Schneier. It operates on 64-bit blocks using a 16-round Feistel network. Its architectural masterpiece is its **Key Expansion** phase: it forces the CPU to execute 521 heavy encryptions just to initialize the cipher state. This acts as a massive "speed bump" that cripples brute-force dictionary attacks, while allowing the actual data encryption to run at blistering, hardware-efficient speeds once the setup is complete.

---

## 2. Technical Features

- **16-Round Feistel Network:** Utilizes a symmetric architecture where the encryption and decryption algorithms are virtually identical. Decryption simply applies the heavily mutated P-array keys in reverse order.
- **Avalanche F-Function:** Splits 32-bit registers into 8-bit quarters and passes them through four distinct S-boxes. By combining the results with mathematically incompatible operations (addition and XOR), changing a single input bit violently scrambles the output.
- **Brute-Force Shield (Key Expansion):** Defends against rapid password guessing by front-loading computational costs. The algorithm recursively encrypts its own subkeys 521 times before it is ready to process actual data.
- **Bitwise Precision & Padding:** Operates strictly on 64-bit boundaries utilizing bitwise masks (`& 0xFFFFFFFF`) to simulate hardware register overflows, alongside PKCS5 padding to perfectly align odd-sized data payloads.

---

## 3. Architecture

```text
.
├── core/                  # Cryptographic Engine
│   ├── __init__.py        # Package initialization
│   └── cipher.py          # Feistel network, F-Function, and Key Expansion logic
├── docs/                  # Technical Documentation
│   ├── logic.md           # XOR reversibility and Pi-derived subkey mutation
│   └── complexity.md      # The "Slow Setup" defense and L1 cache locality bounds
├── test-project/          # Software License Key Encryptor Simulator
│   ├── app.py             # Encrypts and decrypts ML model license payloads with padding
│   └── instructions.md    # Guide for evaluating execution times and ECB mode logic
└── README.md              # Documentation Entry Point

```

---

## 4. Performance Specifications

Let $K$ represent the length of the encryption key and $N$ represent the number of 64-bit data blocks.

| Phase / Metric        | Complexity | Description                                                |
| --------------------- | ---------- | ---------------------------------------------------------- |
| **Key Setup Time**    | $O(K)$     | Intentionally slow; requires 521 block encryptions.        |
| **Block Encryption**  | $O(1)$     | Blazing fast; fixed 16-round bitwise mutations.            |
| **Stream Encryption** | $O(N)$     | Scales perfectly linearly with the file size.              |
| **Space Complexity**  | $O(1)$     | Strictly ~4.1 KB overhead (fits entirely in CPU L1 Cache). |

---

## 5. Deployment & Usage

### Integration

The `BlowfishCipher` can be imported to secure any backend payload prior to transmission:

```python
from core.cipher import BlowfishCipher

# 1. Initialize with a secure backend master key
master_secret = b"SUPER-SECURE-SERVER-KEY"
cipher = BlowfishCipher(master_secret)

# 2. Format the payload (simulating PKCS5 padding for an exact 8-byte block)
# "LICENSE!" is exactly 8 bytes long.
plaintext_payload = b"LICENSE!"

# 3. Encrypt the asset
ciphertext = cipher.encrypt_block(plaintext_payload)
print(f"Encrypted Hex: {ciphertext.hex().upper()}")

# 4. Decrypt on the client side
decrypted_payload = cipher.decrypt_block(ciphertext)
print(f"Recovered: {decrypted_payload.decode('utf-8')}")

```

### Running the Simulator

To observe the profound difference between the slow Key Expansion phase and the lightning-fast encryption phase:

1. Navigate to the `test-project` directory:

```bash
cd test-project

```

2. Run the License Encryptor Simulator:

```bash
python app.py

```

---

## 6. Industrial Applications

- **Password Hashing:** The slow key-expansion architecture of Blowfish directly inspired `bcrypt`, the modern industrial standard for securely storing user passwords in databases.
- **License Key Generation:** Encrypting user IDs, expiration dates, and hardware signatures into a single, unforgeable hexadecimal string.
- **Legacy Secure Storage:** Securing local configuration files, API tokens, and offline database backups where brute-force resistance is prioritized over ultra-high throughput.
