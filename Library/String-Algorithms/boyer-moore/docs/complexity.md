# Complexity Analysis of Boyer-Moore Algorithm

## Time Complexity
*   **Preprocessing (Bad Character Table):** `O(m)` where `m` is the length of the pattern. We iterate through the pattern once.
*   **Searching:**
    *   **Best Case:** `O(n / m)` where `n` is the length of the text. This happens when the algorithm consistently mismatches on the first character it checks (the last character of the pattern) and the mismatched character does not appear in the pattern, allowing it to skip `m` characters ahead every time.
    *   **Worst Case:** `O(n * m)`. This occurs when the text and pattern contain repeated characters, causing the bad character heuristic to provide little to no skipping advantage. (e.g., Text = "AAAAAA", Pattern = "AA"). *Note: A full implementation including the Good Suffix heuristic brings the worst-case time complexity down to O(n).*
    *   **Average Case:** `O(n)` but usually sublinear in practice due to character skipping.

## Space Complexity
*   **O(Σ)** where `Σ` is the size of the alphabet used to store the bad character table. In this dictionary-based implementation, it's `O(m)` because we only store the unique characters present in the pattern.
