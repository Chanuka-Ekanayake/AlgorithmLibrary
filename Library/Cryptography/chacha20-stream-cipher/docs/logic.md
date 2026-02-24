# ChaCha20 Stream Cipher - Logic Overview

## Introduction
ChaCha20 is a widely used stream cipher designed by Daniel J. Bernstein. It is a modification of the Salsa20 algorithm, chosen to improve the diffusion per round while maintaining the exact same high performance. It features a 256-bit key, a 96-bit nonce, and a 32-bit counter.

## How it Works
A stream cipher generates pseudorandom bits (referred to as a "keystream") based on a given key and nonce, which are then XORed with the plaintext to create the ciphertext. Since XOR is its own inverse (`A ^ B = C` and `C ^ B = A`), encryption and decryption in ChaCha20 are mathematically identical.

The process has a simple overarching structure:
1. **State Initialization:** An initial 512-bit state (represented as a 4x4 matrix of 16 x 32-bit words) is created using constants, the 256-bit key, a 32-bit block counter, and a 96-bit nonce.
2. **Rounds Operation:** The initialization state gets mutated securely using 20 rounds of simple operations (addition, XOR, bit rotation).
3. **Serialization:** The resulting state is added to the original unmutated state (to prevent invertibility) and is then serialized into a 64-byte keystream block in little-endian byte order.
4. **XOR:** The keystream block is XORed tightly with 64 bytes of plaintext data. The block counter increments for the next 64 bytes, generating new keystream block.

## The Quarter-Round Operation (`QR`)
The foundation of the entire algorithm is the Quarter-Round operation (`QR(a, b, c, d)`), which takes four 32-bit words as input and operates entirely linearly. No large lookup tables or complex multiplications are needed, which guards against cache-timing side-channel attacks.

```text
a += b; d ^= a; d <<<= 16;
c += d; b ^= c; b <<<= 12;
a += b; d ^= a; d <<<= 8;
c += d; b ^= c; b <<<= 7;
```
*(where `<<<=` is bitwise left rotation).*

## Iterating 20 Rounds
The standard ChaCha20 operates 20 times (alternating between targeting the matrix "columns" vs the matrix "diagonals"):

- **Odd rounds (Columns):** 
`QR(0,4,8,12)`, `QR(1,5,9,13)`, `QR(2,6,10,14)`, `QR(3,7,11,15)`
- **Even rounds (Diagonals):** 
`QR(0,5,10,15)`, `QR(1,6,11,12)`, `QR(2,7,8,13)`, `QR(3,4,9,14)`

This simple combination of addition, rotation, and XOR (ARX) provides fast and highly secure encryption without dedicated crypto CPU instructions (though they do exist for AES).
