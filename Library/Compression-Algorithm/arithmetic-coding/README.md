# Arithmetic Coding Compression

## 1. Overview

**Arithmetic Coding** is an advanced entropy encoding algorithm utilized in high-performance data compression. While traditional algorithms like Huffman Coding translate each character into a discrete series of whole bits (e.g., `A = 01`), Arithmetic Coding encodes an entire message into a single, high-precision fractional number in the range **[0.0, 1.0)**.

By utilizing continuous mathematical interval subdivision, this algorithm can assign _fractional_ bits to symbols. This allows it to compress highly repetitive data down to the theoretical limit of Shannon Entropy, making it vastly superior for long, predictable datasets where assigning a whole bit to a highly probable character would be a mathematical waste.

---

## 2. Technical Features

- **Fractional Bit Allocation:** Surpasses discrete algorithms by natively handling probabilities that don't neatly align with whole-bit boundaries.
- **Arbitrary Precision Management:** Implemented using Python's `decimal` module to manage the massive precision overhead required to prevent floating-point underflow on long strings. Standard 64-bit floats fail after just a few characters; this implementation scales reliably.
- **Dynamic Probability Modeling:** Automatically builds a cumulative distribution table based on the exact frequency of characters in the provided text.
- **Deterministic Decoding:** Reconstructs the exact original string purely from the final fractional number and the predefined target length.

---

## 3. Architecture

```text
.
├── core/                  # Data Compression Engine
│   ├── __init__.py        # Package initialization
│   └── arithmetic.py      # Encoder, Decoder, and Probability logic
├── docs/                  # Technical Documentation
│   ├── logic.md           # Continuous interval subdivision theory
│   └── complexity.md      # Analysis of precision overhead and entropy limits
├── test-project/          # DNA Sequence Compressor Simulator
│   ├── app.py             # Encodes and decodes genetic strings losslessly
│   └── instructions.md    # Guide for evaluating fractional compression
└── README.md              # Documentation Entry Point

```

---

## 4. Performance Specifications

| Metric                  | Specification                                                                                                   |
| ----------------------- | --------------------------------------------------------------------------------------------------------------- |
| **Time Complexity**     | Encoding and decoding: O(n · p), where n is the message length (symbols) and p is the arbitrary-precision scale |
| **Space Complexity**    | O(|Σ| + p), for the probability table over alphabet Σ and the high-precision interval bounds / encoded value    |
| **Compression Ratio**   | Approaches the Shannon entropy limit of the source distribution                                                |
| **Decoding Constraint** | Must know the original message length n to determine when to stop symbol reconstruction                        |

---

## 5. Deployment & Usage

### Integration

The `ArithmeticCoder` class can be integrated into data pipelines to compress strings with small alphabets but massive repetition:

```python
from decimal import Decimal
from core.arithmetic import ArithmeticCoder

# Initialize the coder with a sample text to build probabilities
# Precision is set high to prevent underflow
coder = ArithmeticCoder(text="AABCAA", precision=50)

# Encode the sequence into a single fraction
encoded_fraction = coder.encode("AABCAA")
print(f"Compressed Value: {encoded_fraction}")

# Decode the fraction back to the original string (requires length)
original_text = coder.decode(encoded_fraction, message_length=6)
print(f"Restored Text: {original_text}")

```

### Running the Simulator

To observe the Arithmetic Coder compressing a simulated DNA sequence:

1. Navigate to the `test-project` directory:

```bash
cd test-project

```

2. Run the DNA Compressor:

```bash
python app.py

```

---

## 6. Industrial Applications

- **Video Codecs:** The backbone of the CABAC (Context-Adaptive Binary Arithmetic Coding) engine used in modern H.264 and HEVC video compression standards.
- **Image Compression:** Used in the JPEG 2000 standard to achieve superior compression ratios and higher fidelity over standard JPEG formats.
- **Genomics:** Highly effective for compressing massive DNA datasets featuring very small alphabets (A, C, T, G) where character repetition is immense.
