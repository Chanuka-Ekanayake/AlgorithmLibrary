# AES Simulator Instructions

This project provides an interactive Command Line Interface (CLI) to simulate secure communication and explore block cipher security.

## Running the Simulator

1. Open a terminal and navigate to this directory:
   ```bash
   cd Library/Cryptography/aes-cryptography/test-project
   ```

2. Execute the simulator:
   ```bash
   python app.py
   ```

## What the Simulation Does

1. **Standard Verification**: Automatically runs self-tests with standard AES key sizes (128, 192, 256 bits) to ensure encryption and decryption work flawlessly.
2. **ECB vs. CBC Visualization**: Encrypts a text containing a repeating pattern using both Electronic Codebook (ECB) and Cipher Block Chaining (CBC) modes. It prints the hex outputs side-by-side to visually demonstrate how ECB leaks block patterns (identical blocks encrypt to identical ciphertext), while CBC produces pseudorandom ciphertext.
3. **Performance Benchmarking**: Measures and reports the CPU execution times for key expansion, encryption, and decryption across 128-bit, 192-bit, and 256-bit key sizes.
