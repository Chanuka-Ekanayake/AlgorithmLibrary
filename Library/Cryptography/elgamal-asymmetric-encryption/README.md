# ElGamal Asymmetric Encryption

## 1. Overview

The **ElGamal Cryptosystem** is an asymmetric (public-key) encryption algorithm based on the **Discrete Logarithm Problem (DLP)**. Unlike symmetric algorithms where the same key is shared, ElGamal uses a Public Key for encryption and a distinct Private Key for decryption.

For your marketplace, this algorithm provides a secure method for **Digital Envelopes** and **Software Licensing**. Its defining characteristic is its **probabilistic** nature: because of a random "ephemeral key" used during encryption, the same message will produce a different ciphertext every time it is encrypted. This prevents attackers from identifying patterns in encrypted data.

---

## 2. Technical Features

- **Asymmetric Architecture:** Decouples the encryption and decryption processes, allowing secure communication without a pre-shared secret.
- **Probabilistic Encryption:** Incorporates an ephemeral random variable , ensuring that identical plaintexts result in unique ciphertexts.
- **Discrete Logarithm Security:** Relies on the mathematical "hardness" of reversing modular exponentiation in a cyclic group.
- **Modular Arithmetic Core:** Utilizes high-performance modular exponentiation () and Fermat’s Little Theorem for modular inverses.

---

## 3. Architecture

```text
.
├── core/                  # Cryptographic Engine
│   ├── __init__.py        # Package initialization
│   └── elgamal.py         # KeyGen, Probabilistic Encrypt, and Decrypt logic
├── docs/                  # Technical Documentation
│   ├── logic.md           # Cyclic groups and the Diffie-Hellman relationship
│   └── complexity.md      # Performance analysis of modular exponentiation
├── test-project/          # Secure Licensing Simulator
│   ├── app.py             # Scenario: Issuing a secure software license key
│   └── instructions.md    # Guide for key pair generation and testing
└── README.md              # Documentation Entry Point

```

---

## 4. Performance Specifications

| Metric                     | Specification                                                     |
| -------------------------- | ----------------------------------------------------------------- |
| **Encryption Complexity**  | ≈ 2 modular exponentiations + O(1) multiplications (O(log p))     |
| **Decryption Complexity**  | ≈ 1 modular exponentiation + O(1) multiplications (O(log p))      |
| **Space Overhead**         | 2.0x (Ciphertext is double the size of plaintext)                 |
| **Security Foundation**    | Discrete Logarithm Problem (DLP)                                  |
| **Randomness Requirement** | High (Requires a unique ephemeral key per session)                |

---

## 5. Deployment & Usage

### Integration

The `elgamal` module can be used to protect sensitive numerical data, such as license IDs or hardware fingerprints:

```python
from core.elgamal import ElGamal
from Crypto.Util.number import getPrime

# Initialize with a cryptographically strong 2048-bit prime
p = getPrime(2048)
g = 2  # generator for the multiplicative group modulo p (example choice)
crypto = ElGamal(p=p, g=g)

# Receiver generates their keys
keys = crypto.generate_keys()
public_key = keys["public"]  # (p, g, y)

# Sender encrypts the message
message = 12345
ciphertext = crypto.encrypt(message, public_key)

# Receiver decrypts using their private key
plaintext = crypto.decrypt(ciphertext, keys["private"])

```

### Running the Simulator

To observe the secure license issuance flow:

1. Navigate to the `test-project` directory:

```bash
cd test-project

```

2. Run the Licensing Simulator:

```bash
python app.py

```

---

## 6. Industrial Applications

- **Hybrid Encryption:** Safely exchanging symmetric keys (like AES) over an insecure channel.
- **Digital Signatures:** The foundation for the Digital Signature Algorithm (DSA).
- **Blockchain Privacy:** Used in certain zero-knowledge proof systems and privacy-focused coins.
- **Software Licensing:** Securely delivering activation codes to specific users based on their public keys.
