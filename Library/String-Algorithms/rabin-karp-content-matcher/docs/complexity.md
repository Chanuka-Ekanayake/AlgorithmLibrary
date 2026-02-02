# Complexity Analysis: Rabin-Karp Algorithm

The efficiency of the Rabin-Karp algorithm relies on the **Rolling Hash** technique, which allows us to update the hash value of a sliding window in constant time rather than recomputing it from scratch.

## 1. Time Complexity

| Scenario | Complexity | Description |
| --- | --- | --- |
| **Average Case** |  | When hash collisions are rare, we process each character roughly once. |
| **Best Case** |  | Occurs when the pattern is found early or not at all with minimal collisions. |
| **Worst Case** |  | Occurs if the hash function produces a collision for *every* window (e.g., searching `aaaaa` in `aaaaaaaa`). |

### 1.1 Parameter Breakdown

* **:** Length of the text being searched (the "Haystack").
* **:** Length of the pattern being searched (the "Needle").

### 1.2 The "Rolling" Efficiency

In a naive search, checking a window of length  takes  time. If we do this for every position in a text of length , the total time is .
Rabin-Karp reduces this because:

1. **Initial Hash:** Calculating the first window takes .
2. **Rolling Update:** Each subsequent shift takes **** because we only perform basic arithmetic to "slide" the hash value.
3. **Total:** .

---

## 2. Space Complexity

The space complexity is:


 (Auxiliary Space)

### 2.1 Memory Usage

* The algorithm only stores a few integer variables: the pattern hash, the current window hash, and a few constants (prime, alphabet size, etc.).
* It does not require additional data structures like the  tables in Dynamic Programming or the tree nodes in a Trie.

---

## 3. The Impact of Collisions

A **Hash Collision** occurs when two different strings produce the same hash value.

* **Spurious Hits:** When hashes match but strings don't. The algorithm must perform a character-by-character check () to confirm the match.
* **Mitigation:** We use a large prime number () for the modulo operation. The larger the prime, the lower the probability of collisions, keeping the performance close to .

---

## 4. Comparison with Other Search Algorithms

| Algorithm | Average Time | Space | Best Use Case |
| --- | --- | --- | --- |
| **Naive Search** |  |  | Very short strings. |
| **Rabin-Karp** |  |  | Multiple pattern matching / Plagiarism. |
| **KMP (Knuth-Morris-Pratt)** |  |  | Single pattern, no hashing needed. |
| **Trie Search** |  |  | Prefix matching / Autocomplete. |

---

## 5. Performance Metrics Summary

| Metric | Complexity |
| --- | --- |
| **Pre-processing Time** |  |
| **Matching Time (Avg)** |  |
| **Auxiliary Space** |  |