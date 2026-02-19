# Algorithm Logic: Arithmetic Coding

At its core, Arithmetic Coding abandons the idea of translating individual characters into discrete binary codes (like `A = 01`, `B = 10`). Instead, it treats the entire message as a single, continuous fraction between **0.0** and **1.0**.

## 1. The Probability Table (The Foundation)

Before encoding, the algorithm analyzes the message to determine the frequency of each character. It then partitions the `[0.0, 1.0)` interval, giving larger segments to frequent characters and smaller segments to rare ones.

Let's assume an alphabet with the following probabilities:

- **A** = 60% probability Interval: `[0.0, 0.6)`
- **B** = 20% probability Interval: `[0.6, 0.8)`
- **C** = 20% probability Interval: `[0.8, 1.0)`

---

## 2. The Encoding Process (Shrinking the Interval)

Let's encode the message **"BCA"**.

The algorithm starts with the full interval `[0.0, 1.0)`. As it reads each character, it restricts the current interval to the proportional sub-interval of that character.

**Step 1: Read 'B'**

- Current Interval: `[0.0, 1.0)` (Range = 1.0)
- 'B' corresponds to the middle 20% (`[0.6, 0.8)`).
- **New Interval:** `[0.6, 0.8)` (Range = 0.2)

**Step 2: Read 'C'**

- Current Interval: `[0.6, 0.8)` (Range = 0.2)
- 'C' corresponds to the top 20% (`[0.8, 1.0)` of the base model).
- We must find the top 20% of our _current_ interval.
- New Low =
- New High =
- **New Interval:** `[0.76, 0.80)` (Range = 0.04)

**Step 3: Read 'A'**

- Current Interval: `[0.76, 0.80)` (Range = 0.04)
- 'A' corresponds to the bottom 60% (`[0.0, 0.6)` of the base model).
- We must find the bottom 60% of our _current_ interval.
- New Low =
- New High =
- **Final Interval:** `[0.76, 0.784)`

The entire message "BCA" is now uniquely represented by **any number** within `[0.76, 0.784)`. Typically, encoders just output the lower bound: **0.76**.

---

## 3. The Decoding Process (Expanding the Interval)

To decode **0.76**, the receiver needs the same probability table and the length of the message (3 characters).

**Step 1: Find the First Character**

- Where does `0.76` fall in our base table? It falls inside 'B' `[0.6, 0.8)`.
- **First Character:** 'B'
- Now, we "zoom in" to remove the 'B' influence using the formula:

-

**Step 2: Find the Second Character**

- Where does `0.8` fall in our base table? It falls at the exact start of 'C' `[0.8, 1.0)`.
- **Second Character:** 'C'
- Zoom in again:

**Step 3: Find the Third Character**

- Where does `0.0` fall? It falls at the exact start of 'A' `[0.0, 0.6)`.
- **Third Character:** 'A'

We have reached our target length of 3. The decoded message is exactly **"BCA"**.

---

## 4. The Real-World Application (DNA Compression)

Why go through this trouble? Imagine compressing a DNA sequence containing millions of characters, but only consisting of 'A', 'C', 'T', and 'G'.

Standard ASCII uses 8 bits per character. By treating the millions of characters as one massive fractional sub-division, Arithmetic Coding can compress the entire DNA string into a single decimal number, pushing the file size down to the absolute mathematical limit of entropy.
