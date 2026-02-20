# Complexity Analysis: Manacher’s Algorithm

Manacher’s Algorithm is the optimal solution for the Longest Palindromic Substring problem. It reduces the time complexity from the naive or standard down to strictly linear time.

## 1. Time Complexity

| Algorithm                | Complexity | Bottleneck                                                               |
| ------------------------ | ---------- | ------------------------------------------------------------------------ |
| **Brute Force**          |            | Checks every substring () and verifies if it is a palindrome ().         |
| **Expand Around Center** |            | Expands from every character () potentially to the edges ().             |
| **Manacher’s Algorithm** | \*\*\*\*   | Uses previously computed palindrome radii to skip redundant comparisons. |

### The Proof of Linearity (Amortized Analysis)

The confusion often stems from the nested `while` loop:

```python
while T[i + (1 + P[i])] == T[i - (1 + P[i])]:
    P[i] += 1

```

How can this be ?

1. **The Right Boundary ():** The variable represents the rightmost character of all palindromes found so far.
2. **Monotonic Increase:** The inner `while` loop _only_ executes when we are expanding a palindrome **beyond** the current .
3. **The Limit:** Every time the `while` loop successfully matches characters, increases. Since starts at 0 and cannot exceed the length of the string (), is incremented at most times total.
4. **Conclusion:** Therefore, the total number of operations inside the `while` loop across the _entire_ execution of the algorithm is bounded by .

---

## 2. Space Complexity

| Structure                 | Complexity | Description                                                 |
| ------------------------- | ---------- | ----------------------------------------------------------- |
| **Transformed String ()** |            | The new string with `#` separators is length .              |
| **Radius Array ()**       |            | An integer array storing the radius for each character in . |
| **Total Space**           | \*\*\*\*   | Linear space is required to achieve linear time.            |

---

## 3. Computational Scaling

To understand the massive performance gain, consider a string consisting of 10,000 identical characters (e.g., "AAAA...").

| Input Size () | Expand Around Center ()       | Manacher’s Algorithm ()  |
| ------------- | ----------------------------- | ------------------------ |
| 1,000         | 1,000,000 ops                 | ~2,000 ops               |
| 10,000        | 100,000,000 ops               | ~20,000 ops              |
| 100,000       | 10,000,000,000 ops            | ~200,000 ops             |
| **1,000,000** | **1,000,000,000,000** (Crash) | **~2,000,000** (Instant) |

---

## 4. Engineering Constraints

- **Memory Overhead:** Manacher’s requires allocating a new string roughly the size of the original. For extremely memory-constrained environments (embedded systems with limited RAM), the approach might be preferred purely to save space ( space complexity).
- **Character Sets:** The specific choice of the separator character (`#`) must not appear in the input string, or it must be handled logically. However, in this implementation, the separator is only used to establish positions, so even if `#` appears in the input, the logic holds because `#` will always align with `#`.
