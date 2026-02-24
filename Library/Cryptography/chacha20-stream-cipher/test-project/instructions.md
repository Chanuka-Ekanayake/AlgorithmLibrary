# Running the ChaCha20 Simulation Test Project

## Prerequisites
- **Python 3.6+**: The script uses type hints and recent `time` utilities standard in modern Python distributions.
- No external non-standard dependencies are required (e.g., `pip install`).

## How to Run
Navigate to the root directory of your project (or directly to the `test-project` folder) and execute the standard Python application runner:

```bash
python Library/Cryptography/chacha20-stream-cipher/test-project/app.py
```

## What it does
The simulation acts as a secure messaging system transferring a highly confidential plain text message over an ostensibly insecure simulated network:

1. **Parameters Initialization**: 256-bit randomized root encryption key (`key`) alongside a 96-bit collision-resistant `nonce` is generated.
2. **Setup ChaCha20**: The core encryption logic initiates its mathematical ARX-based setup matrix (Constants + Key + Counter + Nonce).
3. **Encryption Pipeline**: It dynamically translates the payload plaintext message string into an encrypted cipher byte array representation and provides execution performance analytics in milliseconds.
4. **Decryption Pipeline**: Running identical `ChaCha20` object architecture across the decipher routine outputs the reversed plaintext.
5. **Integrity Validation**: Compares origin payload bit sequences against the final evaluated return output payload guaranteeing algorithm structural correctness.
