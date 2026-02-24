# ChaCha20 Complexity Overview

## Time Complexity
The time complexity of ChaCha20 is largely tied to generating the 64-byte keystream block, dependent upon the Quarter-Round operations over 20 rounds. The generated 64 bytes are then used to XOR with the given plaintext.

- **Initialization:** $O(1)$ Setup the 4x4 matrix from a 256-bit key and a 96-bit nonce.
- **Rounds (Block Generation):** $O(1)$ There are exactly 20 rounds of 4 straightforward quarter operations (ARX). This happens in completely constant time and takes up negligible CPU cycles.
- **Overall Complexity:** $O(\lceil N/64 \rceil)$, where $N$ is the number of bytes that require encryption. Time spent grows strictly linearly proportional to the size of the plaintext dataset.

## Space Complexity
- **Overall Space Complexity:** $O(1)$ Auxiliary Space.

Unlike AES algorithms that store massive lookup tables, ChaCha20 keeps virtually no memory other than a working 64-byte 4x4 grid of 32-bit registers, providing an extremely memory-efficient execution context, fitting easily into CPU cache blocks. 

The resulting output can be managed in-place (XOR operation directly replacing memory references space) or $O(N)$ for returning entirely new allocations of the generated cyphertexts and plaintexts.
