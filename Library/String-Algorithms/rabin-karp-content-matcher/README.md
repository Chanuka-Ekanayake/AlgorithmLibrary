# Rabin-Karp Content Matcher

## 1. Overview

The **Rabin-Karp Algorithm** is a high-performance string-searching algorithm that utilizes **Rolling Hashes** to find patterns within a body of text. Unlike naive search methods that require  time, Rabin-Karp operates in near-linear time by "sliding" a mathematical window across the text and updating a numerical fingerprint (hash) in constant time.

This module is specifically designed for **Multi-Pattern Matching**, making it ideal for plagiarism detection, malware signature scanning, and data deduplication.

---

## 2. Technical Features

* **Rolling Hash Engine:** Implements a polynomial rolling hash with modular arithmetic to ensure  hash updates per shift.
* **Multi-Signature Support:** Includes a `batch_search` functionality to scan for an entire library of prohibited signatures in a single pass.
* **Collision Resistance:** Uses a large prime () for the modulo operation and includes a character-by-character "guard" check to handle spurious hash hits.
* **Security Simulator:** A `test-project` that scans Python scripts for common malicious command signatures.

---

## 3. Architecture

```text
.
├── core/                  # Engine Logic
│   └── rabin_karp.py      # Rolling hash and batch search implementation
├── docs/                  # Technical Documentation
│   ├── logic.md           # The math of polynomial hashing and sliding windows
│   └── complexity.md      # Average-case vs. Worst-case analysis
├── test-project/          # Security Simulator
│   ├── app.py             # Malware Signature Scanner CLI
│   ├── library.txt        # Database of prohibited code signatures
│   └── instructions.md    # Operation and testing guide
└── README.md              # Documentation Entry Point

```

---

## 4. Performance Specifications

| Metric | Specification |
| --- | --- |
| **Time Complexity** |  Average |
| **Space Complexity** |  Auxiliary Space |
| **Hash Type** | Polynomial Rolling Hash |
| **Modulus** |  (Prime) |

---

## 5. Deployment & Usage

### Integration

The `RabinKarp` class is highly efficient for scanning unstructured data:

```python
from core.rabin_karp import RabinKarp

scanner = RabinKarp()
text = "The quick brown fox jumps over the lazy dog."
pattern = "brown fox"

matches = scanner.search(pattern, text)
# Result: [10]

```

### Running the Simulator

To execute the Malware Signature Scan:

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

* **Cybersecurity:** Scanning file systems for known malware or virus byte-sequences.
* **Plagiarism Detection:** Identifying exact string matches between student submissions or open-source repositories.
* **Information Retrieval:** Powering "Find in Document" features where multiple keywords need to be highlighted simultaneously.
* **Bioinformatics:** Searching for specific DNA sequences within large genomic datasets.