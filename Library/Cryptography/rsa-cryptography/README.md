# RSA Cryptography

## Description
RSA (Rivest–Shamir–Adleman) is one of the oldest and most widely used public-key cryptosystems for secure data transmission. In a public-key cryptosystem, the encryption key is public and distinct from the decryption key, which is kept secret (private).

## Security Notice
This implementation is for educational purposes and omits critical real-world protections (e.g., OAEP/PKCS#1 padding and side-channel hardening). Do not use it to protect real secrets; use a vetted cryptography library instead.

The security of RSA relies on the practical difficulty of factoring the product of two large prime numbers, the "factoring problem".
## Key Concepts
1.  **Public Key**: Known to everyone and used to encrypt messages.
2.  **Private Key**: Known only to the recipient and used to decrypt messages.
3.  **Prime Number Generation**: The algorithm relies heavily on generating extremely large prime numbers and testing them for primality (e.g., using Miller-Rabin test).

## Applications
- Secure communication protocols (e.g., HTTPS, SSH).
- Digital signatures.
- Key exchange mechanisms.

## Directory Structure
- `core/`: Contains the pure implementation of the RSA algorithm.
- `docs/`: In-depth explanations of the logic and computational complexity.
- `test-project/`: A sample Python script to demonstrate generating keys, encrypting, and decrypting messages using RSA.
