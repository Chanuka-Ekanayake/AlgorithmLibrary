# Boyer-Moore Algorithm

The Boyer-Moore algorithm is an efficient string searching algorithm that is the standard benchmark for practical string search literature. It was developed by Robert S. Boyer and J Strother Moore in 1977. 

The algorithm preprocesses the string being searched for (the pattern), but not the string being searched in (the text). It uses two heuristics to skip sections of the text, resulting in a much faster search compared to naive algorithms:
1. **The Bad Character Heuristic**
2. **The Good Suffix Heuristic** (Currently only the Bad Character heuristic is utilized in this basic implementation for simplicity, which often suffices for practical linear-time-like performance on typical alphabets).

## Features
- **Efficiency**: Skips multiple characters at a time rather than shifting by one.
- **Reverse matching**: Compares the pattern from right to left, making mismatches easily identifiable early.

## Usage (Python)
```python
from core.boyer_moore import search

text = "ABAAABCD"
pattern = "ABC"

occurrences = search(text, pattern)
print("Pattern found at indices:", occurrences)
```
