# Algorithm Logic: Fast Fourier Transform (FFT)

## 1. The Core Strategy: Decimation-in-Time

The FFT works by breaking a Discrete Fourier Transform (DFT) of size into two smaller DFTs of size : one for the **even-indexed** samples and one for the **odd-indexed** samples.

Mathematically, this is based on the **Danielson-Lanczos Lemma**. It proves that the frequency data for a full signal can be reconstructed by combining the frequency data of its sub-signals.

---

## 2. The Butterfly Operation

The "Butterfly" is the fundamental building block of the FFT. It is a specific calculation pattern where the results of two sub-problems are combined using a **Twiddle Factor**.

For each frequency , we compute:

1. **Top Wing:**
2. **Bottom Wing:**

The name "Butterfly" comes from the visual representation of the data flow, where the lines crossing between the even and odd inputs resemble wings. By performing this operation, we calculate two output values for the cost of one complex multiplication.

---

## 3. Twiddle Factors ()

Twiddle factors are complex numbers that represent rotations around the **Unit Circle**.

Since waves are periodic (they repeat every radians), many of the points we calculate in a Fourier Transform are identical or exact opposites of points we've already calculated. The FFT "collects" these common factors and applies them only once, which is the primary source of its speed.

---

## 4. Why must be a Power of 2

Our implementation uses the **Radix-2** method. This requires the input size to be a power of 2 (2, 4, 8, 16...) because the algorithm recursively divides the input by 2 at every step until it reaches a single point.

If a signal is not a power of 2, engineers use **Zero Padding**—adding silent samples to the end of the signal until the next power of 2 is reached.

---

## 5. Domain Transformation

The logic effectively changes the perspective of the data:

- **Time Domain:** A list of "How loud is the sound right now?"
- **Frequency Domain:** A list of "How much of the 440Hz (A4 note) is in this sound?"
