# ChaCha20 Stream Cipher

## Overview
ChaCha20 is an extremely fast and highly secure stream cipher, standardizes in cryptographic applications around the world. It provides equivalent security to AES-256 (a block cipher) but inherently acts differently by running on purely algorithmic CPU addition, rotation, and XOR operations—making it faster on modern machines without specialized encryption instruction sets.

It takes a 256-bit symmetric key, a 96-bit nonce, and an initial block counter.

## Directory Structure
- `core/`: Holds the standard matrix ARX execution model of ChaCha20 (`chacha20.py`).
- `docs/logic.md`: A comprehensive look into how the data generates pseudo-random bits over 20 rounds of constant-time quarter rotations.
- `docs/complexity.md`: Explains precisely why ChaCha20 achieves $O(\lceil N/64 \rceil)$ overall Time & $O(1)$ Space.
- `test-project/`: A simple demonstration verifying payload integrity over a secure encrypted pipeline.

## Get Started
If you're interested in testing or exploring the simulation, navigate to the `test-project/` folder and read its specific `instructions.md`.
