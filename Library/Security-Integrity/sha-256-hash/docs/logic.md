# Algorithm Logic: SHA-256

## 1. The Goal of a Cryptographic Hash
A hash function takes input data of any size and deterministically maps it to a fixed-size string (256 bits for SHA-256). It is designed to act like a digital fingerprint.
- **Deterministic:** The same input always yields the same hash.
- **Fast:** Quick to compute the hash for any given message.
- **Pre-image Resistance:** Given a hash, it is mathematically infeasible to find the original message (One-way).
- **Avalanche Effect:** Changing just one single bit of the input changes roughly 50% of the bits in the output hash.

## 2. The Merkle-Damgård Construction
SHA-256 uses the Merkle-Damgård construction. It breaks the input message into fixed-size blocks (512 bits) and processes them one by one through a **compression function**. 
The output of compressing block 1 becomes the initial state for compressing block 2, chaining them together.

---

## 3. Step-by-Step Algorithm

### Step 1: Padding the Message
SHA-256 strictly processes data in 512-bit chunks. To ensure the message perfectly fits, we pad it:
1. **Append a "1" bit:** The byte `0x80` is appended to the end of the message.
2. **Append "0" bits:** Zeros are added until the total length is exactly 64 bits away from a multiple of 512 (i.e., Length $\equiv$ 448 mod 512).
3. **Append the Original Length:** The original length of the message (in bits) is appended as a 64-bit big-endian integer. The total length is now perfectly divisible by 512.

### Step 2: Message Schedule (W)
For each 512-bit chunk, we break it into sixteen 32-bit words ($w_0$ to $w_{15}$). 
SHA-256 requires 64 words for its 64 rounds of compression, so we "stretch" these 16 words into 64 using bitwise operations:
$$w_i = w_{i-16} + \sigma_0(w_{i-15}) + w_{i-7} + \sigma_1(w_{i-2})$$
Where $\sigma_0$ and $\sigma_1$ are specific combinations of Right-Rotates and Right-Shifts.

### Step 3: The Compression Function (64 Rounds)
The core of SHA-256 maintains 8 state variables ($a, b, c, d, e, f, g, h$), initialized to standard constants (the square roots of the first 8 primes).

For 64 rounds, it scrambles these variables using:
- **Ch (Choose):** `(e AND f) XOR (NOT e AND g)`
  - *If `e` is 1, choose `f`. If `e` is 0, choose `g`.*
- **Maj (Majority):** `(a AND b) XOR (a AND c) XOR (b AND c)`
  - *Returns 1 if the majority of `a, b, c` are 1.*
- **$\Sigma_0$ and $\Sigma_1$:** Complex right-rotations of variables `a` and `e`.

The round constants ($K_i$) are also added to inject non-linear chaos. After 64 rounds, the scrambled variables $a \dots h$ are added back to the original hash values for that chunk.

### Step 4: The Final Hash
Once all 512-bit chunks are processed, the final 8 state variables are simply concatenated together to form the final 256-bit (64 hex character) hash string.

---

## 4. The Avalanche Effect
The non-linear mixing of the $\Sigma$ (Sigma) operations and the 64-round chain ensures that if you flip a single bit in the first byte of the input, that change propagates and multiplies through the message schedule, completely destroying and rewriting the final 256-bit hash. This makes it impossible to guess how a hash will change if you tweak the input.
