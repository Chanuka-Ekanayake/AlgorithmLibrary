# LZW Data Compressor

## 1. Overview

**LZW (Lempel-Ziv-Welch)** is a universal lossless data compression algorithm. It is a dictionary-based algorithm that replaces recurring patterns of characters with single integer codes. Instead of needing to transmit the dictionary alongside the compressed data, LZW builds the dictionary dynamically during both compression and decompression.

This makes it exceptionally elegant and very useful for data streams where the dictionary doesn't need to be sent separately.

---

## 2. Technical Features

* **Dynamic Dictionary:** Automatically builds a dictionary of sequences on-the-fly without needing a pre-computation pass.
* **Lossless Decompression:** Reconstructs the exact dictionary using only the compressed integer codes.
* **End-to-End Pipeline:** Provides both `compress` and `decompress` methods.
* **Algorithmic O(N) Complexity:** The LZW algorithm processes streams in linear time under standard RAM assumptions; this particular implementation may have additional overhead due to practical design choices (e.g., dictionary growth and string handling).

---

## 3. Architecture

```text
.
├── core/                  # Engine Logic
│   └── lzw.py             # LZW compression and decompression logic
├── docs/                  # Technical Documentation
│   ├── logic.md           # Explanation of dynamic dictionary building
│   └── complexity.md      # Analysis of O(N) linear time processing
├── test-project/          # Dictionary Compression Simulator
│   ├── app.py             # File Compression CLI
│   ├── sample_data.txt    # Example repetitive text for testing
│   └── instructions.md    # Operation and testing guide
└── README.md              # Documentation Entry Point
```

---

## 4. Performance Specifications

| Metric | Specification |
| --- | --- |
| **Time Complexity** | `O(N)` (algorithmic, assuming idealized operations; actual runtime depends on this implementation's data structures and string handling) |
| **Space Complexity** | `O(N)` for this implementation (dictionary grows with input); `O(1)` would require an explicitly bounded/resetting dictionary, which is not enabled by default here |
| **Paradigm** | Dictionary-Based Compression |
| **Data Integrity** | 100% Lossless |

---

## 5. Deployment & Usage

### Integration

The `LZWCompressor` is designed for modular use:

```python
from core.lzw import LZWCompressor

coder = LZWCompressor()
compressed_codes, ratio = coder.compress("ABABABABABAB")

original = coder.decompress(compressed_codes)
```

### Running the Simulator

To execute the compression demonstration:

1. Navigate to the `test-project` directory:
```bash
cd test-project
```

2. Run the application:
```bash
python app.py
```

---

## 6. Industrial Applications

* **Image Compression:** LZW is the underlying algorithm for the GIF image format.
* **Archive Formats:** The classic Unix `compress` tool.
* **Document Compression:** Employed in formats like TIFF and early PDF standards for repetitive data handling.
