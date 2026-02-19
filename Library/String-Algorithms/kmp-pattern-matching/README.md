# Knuth-Morris-Pratt (KMP) Pattern Matching

## 1. Overview

The **Knuth-Morris-Pratt (KMP)** algorithm is an advanced string-searching technique designed to find occurrences of a pattern within a main text in linear time.

The fundamental flaw of naive (brute-force) string matching is that it backtracks: when a mismatch occurs, the algorithm throws away all the progress it just made and starts over at the next character. KMP solves this by mathematically guaranteeing that the text pointer _never_ moves backwards. It achieves this by pre-processing the search pattern to understand its own internal repetitions, ensuring that your backend can scan massive documentation files or database entries with absolute, predictable efficiency.

---

## 2. Technical Features

- **Linear Time Execution:** Guarantees performance. It reads the text () and the pattern () exactly once.
- **The LPS Array (Pi Table):** Pre-computes the Longest Proper Prefix which is also a Suffix for every sub-pattern. This tells the algorithm exactly how far to safely "jump" forward when a mismatch occurs.
- **Zero Text Backtracking:** Because the main text pointer only ever increments, KMP is perfectly suited for processing continuous data streams (like reading large files chunk-by-chunk over a network) where rewinding is impossible or expensive.
- **Alphabet Independence:** Unlike other string algorithms that require massive memory tables for large character sets (like Unicode), KMP's memory footprint is strictly tied to the length of the search pattern.

---

## 3. Architecture

```text
.
├── core/                  # String Searching Engine
│   ├── __init__.py        # Package initialization
│   └── kmp.py             # LPS generation and forward-only search logic
├── docs/                  # Technical Documentation
│   ├── logic.md           # Prefix/Suffix theory and Pi Table construction
│   └── complexity.md      # Proof of O(N) search and O(M) preprocessing
├── test-project/          # Model Description Scanner Simulator
│   ├── app.py             # High-speed text scanning and context extraction
│   └── instructions.md    # Guide for evaluating linear search behavior
└── README.md              # Documentation Entry Point

```

---

## 4. Performance Specifications

| Metric                     | Specification                                                         |
| -------------------------- | --------------------------------------------------------------------- |
| **Search Time Complexity** | O(N) (Strictly linear relative to text size)                          |
| **Prep Time Complexity**   | O(M) (Strictly linear relative to pattern size)                       |
| **Space Complexity**       | O(M) (Requires integer array equal to pattern length)                 |
| **Pointer Movement**       | Text pointer strictly increments; Pattern pointer shifts              |

---

## 5. Deployment & Usage

### Integration

The `KMPMatcher` class can be integrated into any text-parsing pipeline to extract all occurrences of a specific string:

```python
from core.kmp import KMPMatcher

# A large block of text (e.g., loaded from a file or database)
database_text = "The quick brown fox jumps over the lazy dog. The dog barks."
search_query = "dog"

# Extract all starting indices in O(N+M) time
match_indices = KMPMatcher.search(database_text, search_query)

print(f"Found {len(match_indices)} matches at indices: {match_indices}")
# Output: Found 2 matches at indices: [40, 49]

```

### Running the Simulator

To observe the KMP algorithm scanning a simulated software package description:

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

- **Text Editors & IDEs:** The underlying logic for "Find" and "Find All" functionalities in large codebase environments without freezing the UI.
- **Command Line Utilities:** Concepts from KMP heavily influence tools like `grep` and `awk`.
- **Network Security:** Used in Intrusion Detection Systems (IDS) to scan network packet payloads in real-time for malicious byte-signatures without dropping packets.
- **Bioinformatics:** Rapidly locating specific, short DNA sequences (genes) within massive genomic strings.
