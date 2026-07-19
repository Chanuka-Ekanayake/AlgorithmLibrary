# Logic of the Boyer-Moore Algorithm

The Boyer-Moore algorithm relies on two main heuristics to achieve its speed: the **Bad Character Heuristic** and the **Good Suffix Heuristic**. 

In our current basic implementation, we focus on the **Bad Character Heuristic**, which is often sufficient for excellent practical performance.

## Bad Character Heuristic
The idea is simple: if a character in the text doesn't match the current character we're checking in the pattern, we can shift the pattern so that the mismatched character in the text aligns with its *last* occurrence in the pattern.

### Preprocessing
We build a table (a hash map or array) mapping every character in the pattern to the index of its last occurrence. 

### Searching Phase
1. We align the pattern with the beginning of the text.
2. We compare the pattern to the text from **right to left** (starting at the last character of the pattern).
3. If all characters match, we've found an occurrence! We record it and shift the pattern to search for more.
4. If a mismatch occurs at index `j` of the pattern (comparing `pattern[j]` with `text[s+j]`):
    * Let `c` be the character in the text `text[s+j]` that caused the mismatch.
    * We look up `c` in our bad character table.
    * If `c` is in the pattern, we shift the pattern so that the last occurrence of `c` in the pattern aligns with `c` in the text.
    * If `c` is not in the pattern, we shift the pattern completely past `c`.
    * *Crucial Detail:* We use a `max(1, j - table[c])` check to ensure we always shift the pattern forward (to the right). If the last occurrence of `c` in the pattern is *after* our current mismatch index `j`, a naive shift would move the pattern backward.

By comparing from right to left, we can immediately identify mismatches at the end of the pattern and skip large chunks of text based on the bad character table.
