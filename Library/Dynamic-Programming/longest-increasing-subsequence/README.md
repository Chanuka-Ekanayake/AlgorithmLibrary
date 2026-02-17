# Longest Increasing Subsequence (LIS)

## 1. Overview

The **Longest Increasing Subsequence (LIS)** is a fundamental algorithmic problem in computer science focused on sequence analysis and data mining. The goal is to find the longest subsequence of a given array where the elements are sorted in strictly increasing order (the elements do not need to be contiguous).

This module is a masterclass in algorithmic optimization. It demonstrates the evolution from a standard **Dynamic Programming** solution to a highly optimized **Binary Search** (Patience Sorting) approach. Crucially, this implementation goes beyond simply returning the _length_ of the sequence; it includes the complex state-tracking required to completely reconstruct the actual sequence of data.

---

## 2. Technical Features

- **Dual Paradigms:** Implements both the educational DP method and the production-grade Binary Search method.
- **Patience Sorting:** Utilizes an abstract "deck of cards" sorting logic to maintain a strictly sorted auxiliary array, allowing for logarithmic search times.
- **Path Reconstruction:** Employs a `parent` tracking array to trace the mathematical lineage of the sequence, enabling full data recovery.
- **Type Safety:** Built with strict Python typing (`List`, `Tuple`) to ensure predictable behavior in large-scale data pipelines.

---

## 3. Architecture

```text
.
├── core/                  # Sequence Analysis Engine
│   ├── __init__.py        # Package initialization
│   └── lis.py             # DP, Binary Search, and Reconstruction logic
├── docs/                  # Technical Documentation
│   ├── logic.md           # Subproblems and Patience Sorting theory
│   └── complexity.md      # Mathematical scaling proof for O(N log N)
├── test-project/          # Stock Trend Analyzer Simulator
│   ├── app.py             # Volatility analysis and performance benchmarking
│   └── instructions.md    # Guide for validating performance differences
└── README.md              # Documentation Entry Point

```

---

## 4. Performance Specifications

| Metric               | Classic DP                | Optimal Binary Search        |
| -------------------- | ------------------------- | ---------------------------- |
| **Time Complexity**  |                           | \*\*\*\*                     |
| **Space Complexity** |                           |                              |
| **Search Mechanism** | Exhaustive Back-tracking  | Bisection / Binary Search    |
| **Scalability**      | Fails on massive datasets | Instantaneous up to millions |

---

## 5. Deployment & Usage

### Integration

The `LongestIncreasingSubsequence` class can be directly imported into data analysis pipelines to extract trends from noisy arrays:

```python
from core.lis import LongestIncreasingSubsequence

# A noisy dataset (e.g., daily active users, stock prices)
dataset = [10, 22, 9, 33, 21, 50, 41, 60, 80]

# Initialize analyzer
analyzer = LongestIncreasingSubsequence()

# Extract the trend using the optimal O(N log N) method
max_length, trend_sequence = analyzer.optimal_binary_search(dataset)

print(f"Trend Length: {max_length}")
print(f"Data Points: {trend_sequence}")
# Output: Data Points: [10, 22, 33, 50, 60, 80]

```

### Running the Simulator

To benchmark the performance difference between the two algorithms:

1. Navigate to the `test-project` directory:

```bash
cd test-project

```

2. Run the Stock Trend Analyzer:

```bash
python app.py

```

---

## 6. Industrial Applications

- **Bioinformatics:** Core logic used in DNA sequence alignment to find common genetic markers.
- **Version Control Systems:** The foundation of the `git diff` utility, calculating the minimum number of insertions and deletions between two text files.
- **Financial Modeling:** Extracting the longest continuous upward or downward trends hidden within highly volatile market data.
- **Mathematics:** Used to solve variations of the Box Stacking Problem and Russian Doll Envelopes problem.
