# Suffix Array + LCP Array

## 1. Overview

The **Suffix Array** is one of the most powerful data structures in string processing. It stores all suffixes of a string in sorted (lexicographic) order, enabling any substring query to be answered in **O(M log N)** time — where M is the query length and N is the text length — after a one-time **O(N log N)** build phase.

The naive approach to substring search — scanning the entire text for every query — costs O(N × M) per query. On real-world datasets (DNA sequences, large codebases, legal corpora), this is simply not viable. The Suffix Array solves this by sorting all N suffixes once, turning every future query into two binary searches on a sorted list.

The **LCP (Longest Common Prefix) Array**, built alongside the Suffix Array in O(N) using Kasai's algorithm, augments the structure to efficiently answer more complex questions: What is the longest substring that appears more than once? What do two documents have in common?

---

## 2. Technical Features

- **O(N log N) Construction:** Uses the Prefix-Doubling (Manber & Myers) technique. Each round doubles the comparison window, completing in `ceil(log₂ N)` passes.
- **O(N) LCP via Kasai's Algorithm:** Exploits the mathematical relationship between adjacent suffixes in text order to carry the LCP count forward, performing only O(N) total character comparisons.
- **O(M log N) Pattern Search:** Two binary searches on the sorted suffix array locate the contiguous block of entries that begin with the query pattern.
- **Longest Repeated Substring:** A single O(N) scan of the LCP array; the maximum value directly gives the answer.
- **Longest Common Substring:** Builds a joint suffix array over the concatenation of two strings and scans the combined LCP array for cross-origin maximum values.

---

## 3. Architecture

```text
.
├── core/                   # String Indexing Engine
│   ├── __init__.py         # Package initialization
│   └── suffix_array.py     # SA construction, LCP (Kasai), search, LRS, LCS
├── docs/                   # Technical Documentation
│   ├── logic.md            # Suffix theory, prefix-doubling walkthrough, Kasai's lemma
│   └── complexity.md       # Full complexity proof and comparison table
├── test-project/           # Plagiarism Detection Engine Simulator
│   ├── app.py              # Multi-scenario demo: search, LRS, LCS
│   └── instructions.md     # Guide for running and interpreting the simulator
└── README.md               # Documentation Entry Point
```

---

## 4. Performance Specifications

| Metric                          | Specification                                                             |
| ------------------------------- | ------------------------------------------------------------------------- |
| **SA Construction**             | O(N log N) — Prefix-doubling, ceil(log₂ N) sorting rounds                |
| **LCP Construction**            | O(N) — Kasai's algorithm, single text-order sweep                        |
| **Pattern Search**              | O(M log N) — Two binary searches on the sorted suffix array              |
| **Longest Repeated Substring**  | O(N) — Linear scan of the LCP array                                      |
| **Longest Common Substring**    | O((N+M) log(N+M)) — Joint suffix array + LCP scan                        |
| **Space Complexity**            | O(N) — SA and LCP arrays, each of length N                               |

---

## 5. Deployment & Usage

### Integration

```python
from core.suffix_array import SuffixArray

text = "the cat sat on the mat by the cat"

# Build once — O(N log N)
sa = SuffixArray(text)

# Query many times — O(M log N) each
positions = sa.search("cat")
print(f"'cat' found at indices: {positions}")
# Output: 'cat' found at indices: [4, 30]

# Longest repeated substring — O(N)
lrs = sa.longest_repeated_substring()
print(f"Longest repeated substring: '{lrs}'")
# Output: Longest repeated substring: 'the cat'

# Longest common substring between two texts — O((N+M) log(N+M))
other = "a cat on a hat"
lcs = sa.longest_common_substring(other)
print(f"Longest common substring: '{lcs}'")
# Output: Longest common substring: ' cat '
```

### Running the Simulator

1. Navigate to the `test-project` directory:

```bash
cd test-project
```

2. Run the Plagiarism Detection Engine:

```bash
python app.py
```

---

## 6. Industrial Applications

- **Plagiarism Detection:** Efficiently find the longest shared substrings between submitted essays and a reference corpus.
- **Bioinformatics:** Locate short DNA probe sequences (e.g., CRISPR guide RNAs) within a full chromosome of 3 billion base pairs; `BWA` and `Bowtie` are both built on Suffix Array variants.
- **Data Compression:** The Burrows-Wheeler Transform (BWT), the backbone of `bzip2` and `xz`, is computed directly from the Suffix Array.
- **Search Engines:** Indexing and retrieving documents by arbitrary substring queries without requiring fixed-vocabulary tokenization.
- **Code Intelligence:** IDEs use suffix-array-like structures to power instant "Find All References" across multi-million-line codebases.
