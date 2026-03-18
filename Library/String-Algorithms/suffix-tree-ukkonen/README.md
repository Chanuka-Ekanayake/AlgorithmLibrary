# Suffix Tree - Ukkonen's Algorithm

## 1. Overview

A **Suffix Tree** is a sophisticated data structure that stores all suffixes of a string $S$ in a tree format, supporting complex string queries in linear time. It's an indispensable tool in bioinformatics, text compression, and advanced search engines.

**Ukkonen's Algorithm** is the standard for $O(N)$ construction. It is an "online" algorithm, meaning it can build the tree character-by-character as they arrive, perfect for streaming data or scenarios where only a prefix of $S$ is known initially.

---

## 2. Technical Features

- **Amortized O(N) Construction Time**: Uses the `Suffix Link` and `Skip/Count` trick to maintain linear build time regardless of alphabet size.
- **O(N) Space Complexity**: Each edge is stored as start/end indices into the original text, ensuring total memory consumption stays proportional to the string length.
- **O(M) Pattern Search**: Independent of the text size $N$, finding a pattern $P$ of size $M$ takes only $O(M)$ character comparisons.
- **Internal Optimization**: Rules like "Once a Leaf, always a Leaf" (Rule 1) and "Early Termination" (Rule 3) drastically reduce unnecessary tree traversals during construction.

---

## 3. Architecture

```text
.
├── core/                   # Suffix Tree Build & Query Engine
│   ├── __init__.py         # Package initialization
│   └── suffix_tree.py      # Ukkonen's Algorithm implementation
├── docs/                   # Detailed Technical Guides
│   ├── logic.md            # Active Point, Rules 1-3, Suffix Links
│   └── complexity.md       # Full O(N) time and space proofs
├── test-project/           # Practical Implementation & Tests
│   ├── app.py              # Suite of test cases and DNA search demo
│   └── instructions.md     # How to run and interpret tests
└── README.md               # Home of the Suffix Tree library
```

---

## 4. Performance Specifications

| Metric | Specification |
| :--- | :--- |
| **Construction** | **O(N)** — Amortized linear time across all phases |
| **Pattern Match** | **O(M)** — Where M is the length of the query pattern |
| **Space Required**| **O(N)** — Constant space per suffix character |
| **Algorithm Type**| **Online / Incremental** |

---

## 5. Usage Example

```python
from core.suffix_tree import SuffixTree

text = "BANANA"
prefix = "ANA"

# Build Tree — O(N)
tree = SuffixTree(text)

# Search — O(M)
if tree.search(prefix):
    print(f"'{prefix}' found in '{text}'!")
```

---

## 6. Industrial Applications

- **Genomic Research**: Fast alignment of DNA/RNA reads.
- **Data Compression**: Efficiently finding repeat patterns in Lempel-Ziv-based compression.
- **Spam Filtering**: Identifying redundant or common patterns in mass-sent emails.
- **Plagiarism Detection**: Spotting exact shared substrings across massive document sets.
- **Text Editors**: Supporting near-instant substring search in huge source files.
