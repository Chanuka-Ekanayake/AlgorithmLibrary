# Complexity Analysis: Aho-Corasick Multi-Pattern Matching

## 1. Construction Time Complexity

| Phase                        | Complexity   | Description                                                                                              |
|------------------------------|--------------|----------------------------------------------------------------------------------------------------------|
| **Trie Construction**        | O(M)         | Each character of each pattern creates or traverses exactly one trie edge. M = total pattern length.    |
| **Failure Link BFS**         | O(M)         | BFS visits every trie node exactly once; failure-link computation per node is O(1) amortised.           |
| **Output Link Inheritance**  | O(M + Z_p)   | Copying output lists during BFS; Z_p = total number of (node, pattern) output pairs across all nodes.  |
| **Total Construction**       | **O(M)**     | Linear in the total length of all patterns.                                                              |

### Why Failure-Link BFS Is O(M)

BFS visits every node exactly once. For each node `v` reached from parent `p` via character `c`, finding `fail(v)` requires walking up `p.fail` chain. In the worst case this looks expensive, but:

- The depth of `fail(p)` is strictly less than the depth of `p`.
- Failure links can only point to shallower nodes.
- The amortised number of upward steps across all nodes in the BFS is bounded by M (the total number of nodes).

Therefore the BFS phase is **O(M)** overall.

---

## 2. Space Complexity

| Structure                   | Complexity          | Description                                                                      |
|-----------------------------|---------------------|----------------------------------------------------------------------------------|
| **Trie nodes**              | O(M)                | At most M nodes (one per character across all pattern insertions).              |
| **Children maps**           | O(M × Σ)            | Σ = distinct characters seen. Dictionary uses only seen characters: O(M) total.|
| **Failure links**           | O(M)                | One pointer per node.                                                            |
| **Output lists**            | O(M + K)            | K = number of patterns; lists inherited via output links can overlap.           |
| **Total**                   | **O(M × Σ)**        | In practice, Σ is small (26 for lowercase alpha, 256 for bytes).               |

> **Note:** Using a fixed-size array of size Σ for children (common in C implementations) gives O(M × Σ) worst-case regardless of input; our Python dictionary gives O(M) nodes with only seen characters stored per node.

---

## 3. Search Time Complexity

| Operation              | Complexity   | Description                                                                                      |
|------------------------|--------------|--------------------------------------------------------------------------------------------------|
| **Automaton traversal**| O(N)         | Each text character moves forward at most once, and failure-link jumps are amortised O(1)/char.|
| **Match reporting**    | O(Z)         | Each match tuple is appended once; Z = total number of pattern occurrences in the text.         |
| **Total Search**       | **O(N + Z)** | Optimal: every character is read once, every match is reported once.                            |

### Amortised O(1) Per Character

Define a potential function Φ = current depth of the automaton state. Per step:
- Each character **increases** depth by at most 1 (one forward edge).
- Each failure-link jump **decreases** depth by at least 1.
- Over N characters, total depth increase ≤ N, so total failure-link jumps ≤ N.

Total transitions ≤ 2N → **O(N)** for the entire search.

---

## 4. Comparison: Single-Pattern vs. Multi-Pattern Matchers

| Approach              | Build Cost      | Search (one text) | Notes                                                       |
|-----------------------|-----------------|-------------------|-------------------------------------------------------------|
| **Brute Force × K**   | O(1)            | O(K × N × L)      | Restart from scratch for every pattern, every mismatch.    |
| **KMP × K**           | O(K × L) = O(M) | O(K × N)          | Each pattern scanned independently; no sharing of work.    |
| **Rabin-Karp × K**    | O(M)            | O(K × N) avg      | Hash collisions add constant factor; K passes over text.   |
| **Suffix Array**      | O(N log N)      | O(M log N) / query| Best for repeated queries on fixed text; one pattern/query.|
| **Aho-Corasick**      | **O(M)**        | **O(N + Z)**      | Single pass regardless of K; optimal for multi-pattern.    |

---

## 5. Scalability Benchmark (Estimated)

Consider scanning N = 1,000,000 bytes against K = 10,000 patterns each of average length L = 8 (M = 80,000):

| Approach              | Build Operations       | Search Operations          | Grand Total          |
|-----------------------|------------------------|----------------------------|----------------------|
| **Brute Force × K**   | 0                      | 10,000 × 1,000,000 × 8     | **80,000,000,000**   |
| **KMP × K**           | 80,000                 | 10,000 × 1,000,000         | **~10,000,080,000**  |
| **Aho-Corasick**      | 80,000                 | 1,000,000 + Z              | **~1,000,080,000**   |

Aho-Corasick is approximately **10,000× faster** than KMP-per-pattern and **80,000× faster** than brute force in this scenario.

> In practice, the Snort IDS scans packets against 60,000+ signatures using Aho-Corasick, achieving microsecond-range scan times that brute-force approaches could not achieve even in milliseconds.

---

## 6. Engineering Constraints

- **Python dict for children**: Each `_TrieNode` uses a `dict` keyed by character. Lookup is O(1) average. For byte-level matching, a 256-element array would give O(1) worst-case and better cache behaviour.
- **Output list copying**: During BFS, we copy the failure-link node's output list into each child. This trades a small amount of extra memory for O(1) output lookup during search (no pointer chasing at query time).
- **Deduplication**: If the same pattern is supplied more than once, it will appear multiple times in results. The caller is responsible for deduplication if needed.
- **Unicode**: Python strings are Unicode; each `char` is a Unicode code point. For multi-byte patterns in UTF-8 encoded bytes, operate on the `bytes` object instead of the decoded string.
