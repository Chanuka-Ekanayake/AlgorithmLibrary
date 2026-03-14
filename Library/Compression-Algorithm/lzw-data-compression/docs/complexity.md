# Complexity Analysis: LZW Compression

LZW Compression is highly efficient for data with many repetitive patterns. Its efficiency stems from generating a single integer code for increasingly long strings of characters.

## 1. Time Complexity

### 1.1 Compression: O(N) on Average (O(N²) Worst-Case for This Implementation)
* **N:** The length of the uncompressed input string.
* During compression, we iterate through the input string exactly once.
* Dictionary lookups (`w + c in dictionary`) take **O(1)** time on average when using Hash Maps (like Python dictionaries) or Tree-based Tries (Trie structures guarantee O(L) where L is pattern length, but since we step char-by-char, it amortizes to O(1) per step).
* In our Python reference implementation, we repeatedly build new strings via expressions like `wc = w + c`. Since string concatenation copies the existing contents, this can lead to **O(N²)** behavior in the worst case (for example, on highly repetitive inputs where `w` becomes very long).
* Overall Time Complexity (current implementation): **O(N)** on average, **O(N²)** in the worst case due to string concatenation.

### 1.2 Decompression: O(N)
* **N:** The length of the decompressed string (or effectively the number of compressed codes C, where C <= N).
* We iterate through the list of compressed codes exactly once.
* Extracting from the dictionary and appending the new sequence are **O(1)** average-case operations.
* String concatenations can theoretically take longer if we aren't careful, but efficiently implemented (using `"".join()` instead of `+=`), it remains **O(N)**.
* Overall Time Complexity: **O(N)**.

---

## 2. Space Complexity

The space complexity is determined by the size of the dictionary built during execution.

* **Space Complexity:** **O(N)** in the worst-case scenario.
* Every time we read a character that forms a new sequence, we add exactly one new entry to the dictionary.
* In the absolute worst-case scenario (a string with no repeating patterns), we might add up to N entries to the dictionary.
* However, in practical implementations (like GIF), the dictionary size is strictly capped (e.g., maximum 4096 entries, using 12-bit codes). When the dictionary fills up, the algorithm either clears it and starts over or stops adding new entries. If a bounded dictionary is used, Space Complexity is **O(1)** (constant limit).

---

## 3. Performance Metrics Table

| Metric | Complexity | Note |
| --- | --- | --- |
| **Compression Time** | O(N) avg, O(N²) worst-case | String concatenation in the current Python implementation can cause superlinear behavior on some inputs. |
| **Decompression Time** | O(N) | Very fast. |
| **Space Complexity** | O(N) | Can be O(1) if dictionary size is strictly capped. |
| **Data Types** | Text strings (Python `str`, e.g., UTF-8 text) | Very effective on repetitive text/images. |

---

## 4. Engineering Trade-offs

* **Pros:** Typically very fast compression and decompression (linear-time behavior in the average/ideal case); requires zero pre-computation (no frequency analysis needed); the dictionary does not need to be transmitted alongside the file.
* **Cons:** In the current Python implementation, compression can degrade to superlinear time on certain highly repetitive inputs due to repeated string concatenation; performs poorly (and can actually *increase* file size) on highly random or previously compressed data, because it takes time to populate the dictionary with useful sequences; requires careful memory management in memory-constrained embedded systems if dictionary bounding is not implemented.
