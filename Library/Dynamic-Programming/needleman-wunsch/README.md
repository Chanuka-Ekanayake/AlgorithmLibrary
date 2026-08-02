# Needleman-Wunsch Algorithm

## Overview
The Needleman-Wunsch algorithm is a classic dynamic programming algorithm used in bioinformatics to align protein or nucleotide sequences. It performs a **global alignment**, meaning it aligns every residue in every sequence, finding the best possible alignment across the entire length of the sequences.

## How It Works
The algorithm works in three main steps:
1. **Initialization:** A scoring matrix is created, and the first row and column are initialized with gap penalties.
2. **Matrix Filling:** The rest of the matrix is filled using a scoring system for matches, mismatches, and gaps. Each cell takes the maximum score from its adjacent cells (diagonal for match/mismatch, top/left for gap).
3. **Traceback:** Starting from the bottom-right of the matrix, the optimal path back to the top-left is traced to construct the final alignment strings.

## Implementation Detail
The `needleman_wunsch.py` file contains a Python implementation.

### Parameters:
- `match_score` (default: 1): Score added for matching characters.
- `mismatch_score` (default: -1): Score subtracted for mismatching characters.
- `gap_penalty` (default: -1): Score subtracted for introducing a gap.

## Example Usage
```python
from needleman_wunsch import needleman_wunsch

seq1 = "GATTACA"
seq2 = "GCATGCU"
aligned_1, aligned_2, score = needleman_wunsch(seq1, seq2)

print(aligned_1) # G-ATTACA
print(aligned_2) # GCA-TGCU
print(f"Score: {score}")
```
