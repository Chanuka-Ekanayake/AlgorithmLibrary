# User Guide: SHA-256 Simulator

This project demonstrates the core properties of the **SHA-256 Cryptographic Hash Function**. It contains a pure Python implementation of the actual bitwise math used to compress data securely.

## What You'll See

The simulator runs two interactive demonstrations:

### Demo 1: The Avalanche Effect
You will see how a standard sentence is hashed into a 64-character string. Then, you'll see what happens to the hash when you make a microscopic change to the input (e.g., changing a single letter from uppercase to lowercase, or appending a period). The resulting hash completely changes, proving that it is impossible to predict the output based on the input.

### Demo 2: Proof-of-Work (Bitcoin Miner Simulator)
Cryptocurrencies like Bitcoin secure their networks using SHA-256. "Miners" compete to combine transaction data with a random number (a *nonce*) until the resulting SHA-256 hash starts with a specific number of zeros. 
Because the hash output is completely unpredictable (due to the Avalanche Effect), the only way to find this specific hash is by brute-forcing thousands of combinations. You will watch the pure Python algorithm simulate this process in real time.

## How to Test

1. **Navigate** to the `test-project` folder.
2. **Run** the simulator:
   ```bash
   python app.py
   ```
