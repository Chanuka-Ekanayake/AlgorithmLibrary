# Algorithm Logic: Blowfish (Symmetric Cipher)

Blowfish is a symmetric-key block cipher. This means the exact same key is used to both lock (encrypt) and unlock (decrypt) the data, and the data is processed in fixed 64-bit (8-byte) chunks called "blocks".

## 1. The Feistel Network: 16 Rounds of Chaos

The core architecture of Blowfish is a 16-round Feistel Network. A Feistel network is a cryptographic structure that splits a block of data into two equal halves—Left ($L$) and Right ($R$)—and iteratively mixes them.

For a 64-bit block of data:

1. **Split:** The 64 bits are divided into a 32-bit Left half ($L_0$) and a 32-bit Right half ($R_0$).
2. **The XOR Mix:** In each of the 16 rounds, the Left half is XORed with a pre-calculated subkey from the P-array ($P_i$).
3. **The Function:** The result is passed through a mathematical "mixer" called the F-Function.
4. **The Crossover:** The output of the F-Function is XORed with the Right half.
5. **The Swap:** The Left and Right halves are swapped for the next round.

Mathematically, a single round looks like this:

$$L_{i} = L_{i-1} \oplus P_i$$

$$R_{i} = R_{i-1} \oplus F(L_i)$$

$$Swap(L_i, R_i)$$

### The Magic of Decryption

Why use a Feistel Network? Because **XOR is perfectly reversible**.
If you XOR a value twice with the same key, you get the original value back ($A \oplus B \oplus B = A$). Because of this mathematical property, the hardware or software doesn't need a separate "decryption" algorithm. To decrypt the ciphertext, you simply run the exact same 16-round encryption process, but you apply the P-array keys in reverse: the 16 rounds use $P_{17}$ down to $P_2$, followed by final XORs with $P_{1}$ and $P_{0}$.

---

## 2. The F-Function (The Mixer)

The Feistel Network dictates _how_ the data moves, but the F-Function is what actually scrambles it. It takes a 32-bit input, shatters it into pieces, and runs it through the S-boxes (Substitution boxes).

1. **Shatter:** The 32-bit input is split into four 8-bit quarters: $a, b, c, d$.
2. **Substitute:** Each 8-bit quarter is used as an index (from 0 to 255) to look up a new 32-bit value in one of the four S-boxes.
3. **Combine:** The results are combined using alternating addition and XOR operations.

The mathematical formula for the F-Function is:

$$F(x) = (((S_1[a] + S_2[b]) \pmod{2^{32}}) \oplus S_3[c]) + S_4[d] \pmod{2^{32}}$$

Because addition and XOR are mathematically incompatible (they don't easily distribute over one another), combining them creates intense non-linearity. Changing even a single bit in the input causes a massive, unpredictable "avalanche" of changes in the output.

---

## 3. Key Expansion: The Brute-Force Shield

If Blowfish is so fast, what stops a hacker from writing a script to guess millions of passwords per second? The answer is the **Key Expansion** phase.

Before you can encrypt a single byte of data, the algorithm must initialize its state. It starts with a standard P-array (18 entries) and four S-boxes (1024 entries), populated with the fractional digits of Pi ($\pi$).

To securely inject the user's password into the cipher, it does the following:

1. **XOR the Key:** The P-array is XORed with the user's key.
2. **Encrypt Zeroes:** It takes a 64-bit block of absolute zeroes and encrypts it using the current (weak) state of the cipher.
3. **Replace P-Array:** The resulting encrypted block replaces $P_0$ and $P_1$.
4. **Encrypt the Output:** It takes that newly encrypted block and encrypts it _again_.
5. **Replace Next:** The new result replaces $P_2$ and $P_3$.

This process repeats **521 times** until the entire P-array and all four S-boxes have been replaced by heavily encrypted data.

Because the setup requires 521 consecutive encryptions before the cipher is even ready to use, Blowfish acts as a massive speed bump against brute-force attacks. While it encrypts data instantly once initialized, the slow startup makes rapidly guessing keys computationally exhausting.
