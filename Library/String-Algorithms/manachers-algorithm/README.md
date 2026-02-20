# Manacher's Algorithm

## 1. Overview

Finding the longest palindromic substring is a classic computational problem. Standard "expand around center" approaches operate in time, which becomes an immediate bottleneck when parsing massive texts or genomic sequences.

**Manacher's Algorithm** is an elite dynamic programming solution that flattens this problem into strict ** linear time**.

It solves two massive headaches in string processing simultaneously:

1. **The Even/Odd Problem:** By preprocessing the string and injecting dummy characters (e.g., transforming `"abba"` into `"^#a#b#b#a#$"`), it guarantees that every palindrome has a distinct, physical center, allowing a single mathematical logic loop to process everything uniformly.
2. **Redundant Comparisons:** By tracking the center and rightmost boundary of previously discovered palindromes, it uses mathematical symmetry to physically "mirror" known palindrome radii. If a character falls within a known boundary, the algorithm skips the manual character-by-character check entirely.

---

## 2. Technical Features

- **Linear Time Execution:** Guarantees performance via amortized boundary tracking ( and ). The inner `while` loop only executes when pushing the absolute right boundary forward, meaning it runs a maximum of times across the _entire_ algorithm.
- **Sentinel Injection:** Uses `^` and `$` at the absolute bounds of the transformed string to naturally prevent `IndexOutOfBounds` errors during expansion, saving expensive `if` checks in the inner loop.
- **Symmetry Exploitation:** Implements the mathematical formula `mirror = 2 * C - i` to instantly copy valid palindrome lengths from the left side of a known boundary to the right side.

---

## 3. Architecture

```text
.
├── core/                  # String Searching Engine
│   ├── __init__.py        # Package initialization
│   └── manacher.py        # Boundary tracking and linear scan logic
├── docs/                  # Technical Documentation
│   ├── logic.md           # Preprocessing tricks and symmetry mirroring
│   └── complexity.md      # Amortized proof of O(N) while-loop execution
├── test-project/          # Genomic Palindrome Scanner Simulator
│   ├── app.py             # High-speed DNA structure extraction
│   └── instructions.md    # Guide for evaluating performance constraints
└── README.md              # Documentation Entry Point

```

---

## 4. Performance Specifications

| Metric                   | Specification                                         |
| ------------------------ | ----------------------------------------------------- |
| **Time Complexity**      | \*\*\*\* (Strictly linear via boundary tracking)      |
| **Space Complexity**     | (Requires preprocessed string and radius array)       |
| **Bottleneck Addressed** | Eliminates redundant center expansions                |
| **Core Mechanism**       | Amortized dynamic programming / String transformation |

---

## 5. Deployment & Usage

### Integration

The `Manacher` class can be directly imported into bioinformatics pipelines or text analyzers to extract symmetrical sequences instantly:

```python
from core.manacher import Manacher

# A sample data sequence (e.g., DNA base pairs or text)
data_stream = "ACGTACGTACGTGATTACACATTAGCGTAC"

# Extract the longest palindrome in O(N) time
longest_pal = Manacher.find_longest_palindrome(data_stream)

print(f"Extracted Sequence: {longest_pal}")
print(f"Length: {len(longest_pal)}")
# Output: Extracted Sequence: GATTACACATTAG
# Output: Length: 13

```

### Running the Simulator

To observe the algorithm extracting genetic structures without triggering massive nested loops:

1. Navigate to the `test-project` directory:

```bash
cd test-project

```

2. Run the Scanner:

```bash
python app.py

```

---

## 6. Industrial Applications

- **Bioinformatics:** Identifying palindromic sequences in DNA and RNA, which frequently correspond to restriction enzyme cutting sites, CRISPR arrays, or regulatory sequences.
- **Data Compression:** Identifying repeating, symmetrical data structures prior to applying dictionary-based compression algorithms (like LZ77 or LZ78) to optimize the encoding dictionary.
- **Text Analysis:** Core utility in advanced Natural Language Processing (NLP) pipelines that require rapid structural analysis of massive document corpora.
