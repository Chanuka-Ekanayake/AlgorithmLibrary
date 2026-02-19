# Complexity Analysis: Arithmetic Coding

While Huffman Coding is fast and simple, it is mathematically constrained because it must assign at least one whole bit to every symbol. Arithmetic Coding breaks this barrier. By encoding the entire message into a single continuous interval, it can assign _fractional_ bits to symbols, allowing it to reach the absolute theoretical limit of data compression: **Shannon Entropy**.

## 1. Time Complexity

| Phase                | Complexity | Description                                                                                                                    |
| -------------------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------ |
| **Table Generation** |            | Requires scanning the text of length to find frequencies, then sorting the unique characters to build deterministic intervals. |
| **Encoding**         |            | Iterates through the message of length . represents the overhead of arbitrary-precision floating-point arithmetic.             |
| **Decoding**         |            | For each of the characters, it must check which of the character intervals contains the current fractional value.              |

### The Precision Overhead ()

In standard algorithms, mathematical operations (like addition or multiplication) take time because they use fixed 64-bit hardware registers.

Arithmetic Coding, however, requires **Arbitrary-Precision Arithmetic**. If a message is 1,000 characters long, the resulting decimal might need 3,000 digits of precision to avoid underflow. Multiplying 3,000-digit numbers in software is significantly slower than standard hardware math. This precision overhead () makes Arithmetic Coding highly CPU-intensive compared to dictionary-based methods like LZ77.

---

## 2. Space Complexity

| Component             | Complexity | Description                                                                                                     |
| --------------------- | ---------- | --------------------------------------------------------------------------------------------------------------- |
| **Probability Table** |            | Stores the `[low, high)` decimal boundaries for each unique character .                                         |
| **Encoded Message**   | bits       | While it outputs a "single number," that number requires bits of memory to store its massive decimal precision. |

---

## 3. The Entropy Advantage (Fractional Bits)

To understand the mathematical superiority of this algorithm, consider a file where the letter "A" makes up 99% of the data.

According to Information Theory, the optimal number of bits to represent a symbol with probability is .

- For "A" (): Optimal size is **~0.014 bits**.
- **Huffman Coding:** Forces "A" to take **1 whole bit** (a massive 7000% waste of space).
- **Arithmetic Coding:** Subdivides the interval by 0.99, effectively encoding "A" using the mathematically perfect **~0.014 bits**.

This is why Arithmetic Coding is the underlying entropy encoder for modern, ultra-efficient formats like JPEG 2000 and H.264/HEVC video codecs.

---

## 4. Engineering Trade-offs

- **Error Propagation:** If a single bit in the encoded fractional number is flipped during transmission, the entire rest of the message will decode into garbage. It requires strict error-correcting codes (like Reed-Solomon) when sent over networks.
- **Lack of Random Access:** You cannot decode the 500th character of an arithmetic-encoded message without first decoding characters 1 through 499.
- **Integer Implementation:** In production systems (like C++ video codecs), the arbitrary-precision decimal math is usually simulated using clever 32-bit or 64-bit integer shifting techniques to avoid the massive CPU overhead of software-based floating points.
