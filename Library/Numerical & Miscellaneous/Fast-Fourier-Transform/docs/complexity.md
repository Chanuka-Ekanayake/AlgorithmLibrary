# Complexity Analysis: Fast Fourier Transform (FFT)

The Fast Fourier Transform is a highly optimized algorithm for computing the Discrete Fourier Transform. Its efficiency stems from exploiting the symmetry and periodicity of complex roots of unity.

## 1. Time Complexity

| Algorithm              | Complexity | Operations for |
| ---------------------- | ---------- | -------------- |
| **Naive DFT**          |            | ~1,048,576     |
| **FFT (Cooley-Tukey)** | \*\*\*\*   | **~10,240**    |

### 1.1 The Proof

1. **Divide:** At each step, the problem is split into two halves (). There are such steps before reaching the base case of .
2. **Combine:** At each level of the recursion, we perform operations (the "Butterfly" additions and multiplications).
3. **Total:** multiplying the work per level () by the number of levels () gives the final complexity of \*\*\*\*.

---

## 2. Space Complexity

| Requirement              | Complexity | Description                                                                            |
| ------------------------ | ---------- | -------------------------------------------------------------------------------------- |
| **Auxiliary Space**      |            | In a recursive implementation, the call stack and intermediate lists consume memory.   |
| **In-Place (Iterative)** |            | Advanced iterative versions can perform the transform within the original input array. |
| **Input/Output**         |            | Storing the complex numbers for the time and frequency domains.                        |

---

## 3. Computational Scaling

The FFT's advantage grows exponentially as the sample size increases. This is why it is used for high-resolution audio (44.1kHz) and image processing.

| Samples () | Naive Ops ()  | FFT Ops () | Speedup Factor |
| ---------- | ------------- | ---------- | -------------- |
| 16         | 256           | 64         | 4x             |
| 256        | 65,536        | 2,048      | 32x            |
| 4,096      | 16,777,216    | 49,152     | 341x           |
| 65,536     | 4,294,967,296 | 1,048,576  | **4,096x**     |

---

## 4. Engineering Constraints

- **Radix-2 Requirement:** Our implementation requires the input length to be a power of (). For non-power-of-2 signals, "zero-padding" is typically used to reach the next power of 2.
- **Precision:** Because the algorithm involves many complex multiplications, floating-point rounding errors can accumulate in very large datasets. For precision-critical ML models, 64-bit floats are standard.
- **Locality of Reference:** The recursive "Decimation-in-Time" structure is cache-friendly, making it perform better on modern CPUs than naive matrix multiplication.
