# Complexity Analysis: Suffix Array + LCP Array

## 1. Construction Time Complexity

| Phase                            | Complexity   | Description                                                                                   |
| -------------------------------- | ------------ | --------------------------------------------------------------------------------------------- |
| **Suffix Array (Prefix-Doubling)** | O(N log N)   | ceil(log₂ N) rounds, each involving an O(N log N) sort and an O(N) rank-reassignment pass.   |
| **LCP Array (Kasai's)**          | O(N)         | Single sweep over text in original order; LCP counter decrements by at most 1 per character. |
| **Total Construction**           | **O(N log N)** | Dominated by the Suffix Array construction phase.                                           |

### Why Prefix-Doubling is O(N log N)

- In each of the `ceil(log₂ N)` rounds, the algorithm sorts N elements using a comparison function that runs in O(1) (comparing pre-computed integer rank pairs).
- Each sort is O(N log N) using Python's Timsort.
- Total: O(N log N × log N rounds) = O(N log² N) with a naive sort, but with radix sort it reduces to O(N log N). Our implementation uses Python's built-in sort for clarity.

> **Note:** The theoretically optimal DC3/Skew algorithm achieves O(N) construction, but prefix-doubling is preferred in practice for its simplicity and excellent constant factors.

---

## 2. Space Complexity

| Structure           | Complexity | Description                                             |
| ------------------- | ---------- | ------------------------------------------------------- |
| **Suffix Array**    | O(N)       | One integer per suffix.                                 |
| **LCP Array**       | O(N)       | One integer per adjacent pair of suffixes.              |
| **Rank / Temp Arrays** | O(N)    | Working arrays reused during construction; discarded after. |
| **Total**           | **O(N)**   | Linear in the length of the input string.               |

---

## 3. Query Time Complexity

| Operation                        | Complexity      | Method                                         |
| -------------------------------- | --------------- | ---------------------------------------------- |
| **Pattern Search**               | O(M log N)      | Two binary searches on the sorted suffix array.|
| **Longest Repeated Substring**   | O(N)            | Linear scan of the LCP array for its maximum.  |
| **Longest Common Substring**     | O((N+M) log(N+M)) | Joint suffix array construction + LCP scan.  |

---

## 4. Comparison: Naive vs. Suffix Array vs. Other Libraries

| Approach              | Build Cost | Query Cost (per pattern) | Notes                                           |
| --------------------- | ---------- | ------------------------ | ----------------------------------------------- |
| **Brute Force**       | O(1)       | O(N × M)                 | No preprocessing; collapses on repeated queries.|
| **KMP**               | O(M)       | O(N)                     | Optimal for a single pattern, single text pass. |
| **Trie of Suffixes**  | O(N²)      | O(M)                     | Fastest query, but impractical memory: O(N²).   |
| **Suffix Array + LCP**| O(N log N) | O(M log N)               | Best build/query trade-off; O(N) memory.        |
| **Suffix Automaton**  | O(N)       | O(M)                     | Optimal, but significant implementation complexity.|

---

## 5. Scalability Benchmark (Estimated)

Consider building once and answering 1,000 queries, each of length M = 50, on a text of N = 1,000,000 characters:

| Approach         | Build Operations   | Total Query Operations     | Grand Total        |
| ---------------- | ------------------ | -------------------------- | ------------------ |
| **Brute Force**  | 0                  | 1,000 × 1,000,000 × 50     | **50,000,000,000** |
| **Suffix Array** | ~20,000,000 (N log N) | 1,000 × 50 × 20 (M log N) | **~21,000,000**    |

The Suffix Array approach is approximately **2,380× faster** in this scenario.

---

## 6. Engineering Constraints

- **Sentinel Character:** The implementation appends `'$'` (ASCII 36) to ensure all suffixes are unique. Any character guaranteed to be lexicographically smaller than all characters in the input would work.
- **Python Sort Stability:** Python's Timsort is stable and adaptive. For nearly-sorted inputs (common in later prefix-doubling rounds), it performs significantly better than O(N log N) in practice.
- **Memory vs. Speed:** For texts larger than ~100MB, consider using a C-extension like `pydivsufsort` which implements the linear-time SA-IS algorithm with a tiny memory footprint.
