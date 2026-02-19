# Complexity Analysis: Knuth-Morris-Pratt (KMP)

The fundamental flaw in a Brute-Force string search is "backtracking." When a mismatch occurs, the brute-force algorithm moves the text pointer all the way back to the start of the last attempted match and tries again. KMP eliminates text backtracking entirely.

## 1. Time Complexity

| Phase                         | Complexity | Description                                                                                                            |
| ----------------------------- | ---------- | ---------------------------------------------------------------------------------------------------------------------- |
| **Preprocessing (LPS Array)** |            | Iterates through the pattern (length ) exactly once to build the Longest Prefix Suffix array.                          |
| **Searching Execution**       |            | Iterates through the text (length ). The text pointer `i` only ever moves forward or stays still; it never decrements. |
| **Total Time Complexity**     | \*\*\*\*   | The absolute worst-case scenario is a linear sum of both lengths.                                                      |

### The Mathematical Proof of Search

In the search phase, the `while` loop condition is bounded by the text length . Inside the loop:

1. If characters match, both text pointer `i` and pattern pointer `j` increment.
2. If characters mismatch, `j` falls back using the LPS array (`j = lps[j-1]`), but **`i` does not change**.
3. Because `i` only ever increments and never decrements, the maximum number of times the loop can increment `i` is exactly .

Therefore, the search phase executes in strict time.

---

## 2. Space Complexity

| Requirement   | Complexity | Description                                                                          |
| ------------- | ---------- | ------------------------------------------------------------------------------------ |
| **LPS Array** | O(M)       | An integer array of the exact same length as the search pattern is stored in memory. |
| **Pointers**  | O(1)       | Only a few integer variables (`i`, `j`, `length`) are maintained during execution.   |

**The Memory Trade-off:**
KMP trades a small amount of memory () to achieve its massive speedup. Since search patterns (like a software model name or a specific tag) are typically very short compared to the text being searched, this memory footprint is entirely negligible in real-world systems.

---

## 3. Computational Scaling (Brute Force vs. KMP)

Consider searching for a 100-character pattern within a 1,000,000-character text file.

| Algorithm       | Worst-Case Operations | Bottleneck                                                     |
| --------------- | --------------------- | -------------------------------------------------------------- |
| **Brute Force** | operations            | - Fails heavily on texts with many repeating similar prefixes. |
| **KMP**         | ** operations**       | - Processes the text in a single, clean sweep.                 |

---

## 4. Engineering Constraints

- **Alphabet Independence:** Unlike the Boyer-Moore algorithm (which relies on a "bad character" table that scales with the size of the alphabet/character set), KMP's memory and time complexities are completely independent of the alphabet size. It works just as efficiently on Binary data (0s and 1s) as it does on full UTF-8 text.
- **Stream Processing:** Because the text pointer `i` never moves backwards, KMP is exceptionally well-suited for processing **streams** of data (like reading a massive file chunk by chunk from a hard drive or network socket) where backtracking is impossible or highly expensive.
