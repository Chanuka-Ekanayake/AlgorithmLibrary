# Z-Algorithm (Linear Pattern Matching)

## 1. Overview

The **Z-Algorithm** is a sophisticated string-searching algorithm that finds all occurrences of a `pattern` within a `text` in **linear time** (). In traditional naive searches, repetitive text (common in source code or genomic data) causes the search to slow down significantly as it re-scans characters.

The Z-algorithm solves this by constructing a **Z-array** using a "Z-box" windowing strategy. This allows the algorithm to "remember" previous matches and skip unnecessary comparisons, making it as efficient as the industry-standard KMP algorithm but with a more intuitive structural logic.

---

## 2. Technical Features

- **Guaranteed Linear Time:** Every character in the combined search string is compared at most twice, ensuring a performance bound of .
- **The Z-Box Optimization:** Uses a sliding window to track the rightmost match of the string's prefix, allowing the algorithm to leapfrog over characters it has already "seen."
- **Alphabet Independence:** Unlike some algorithms that depend on the size of the character set, the Z-algorithm works identically on ASCII, Unicode, or raw binary data.
- **Concatenation Pattern:** Utilizes the concatenation trick to transform an external search problem into a localized self-prefix problem.

---

## 3. Architecture

```text
.
├── core/                  # Pattern Matching Engine
│   ├── __init__.py        # Package initialization
│   └── z_search.py        # Z-array construction and matching logic
├── docs/                  # Technical Documentation
│   ├── logic.md           # Detailed breakdown of Z-box cases (L, R)
│   └── complexity.md      # Mathematical proof of O(n + m) time
├── test-project/          # Deep Code Search Simulator
│   ├── app.py             # High-speed search across repetitive ML scripts
│   └── instructions.md    # Guide for benchmarking search performance
└── README.md              # Documentation Entry Point

```

---

## 4. Performance Specifications

| Metric                 | Specification                             |
| ---------------------- | ----------------------------------------- |
| **Search Complexity**  |                                           |
| **Space Complexity**   |                                           |
| **Preprocessing Time** | Included in Linear Pass                   |
| **Matching Style**     | Exact, Case-Sensitive                     |
| **Best For**           | Large-scale codebases, Logs, and Metadata |

---

## 5. Deployment & Usage

### Integration

The `z_search` function is ready to be integrated into your marketplace's backend for metadata indexing or file scanning:

```python
from core.z_search import z_search

text = "def calculate_loss(y_true, y_pred): return sum((y_true - y_pred)**2)"
pattern = "calculate_loss"

# Returns a list of all starting indices where the pattern is found
matches = z_search(text, pattern)

print(f"Found {len(matches)} occurrences at indices: {matches}")

```

### Running the Simulator

To see the Z-algorithm scan a simulated repository of ML models in linear time:

1. Navigate to the `test-project` directory:

```bash
cd test-project

```

2. Run the Code Search tool:

```bash
python app.py

```

---

## 6. Industrial Applications

- **IDE Search Engines:** Powering "Find in Project" features in modern code editors.
- **Bioinformatics:** Identifying specific DNA sequences (motifs) within massive genomic datasets.
- **Data Compression:** Finding repeated substrings to optimize dictionary-based compression (like LZ77).
- **Log Analysis:** Rapidly scanning terabytes of server logs for specific error patterns or security threats.
