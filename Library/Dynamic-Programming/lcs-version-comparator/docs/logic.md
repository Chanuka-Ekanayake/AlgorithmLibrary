# Algorithm Logic: Longest Common Subsequence (LCS)

## 1. The Core Concept

The **Longest Common Subsequence** algorithm identifies the longest set of elements that appear in the same relative order in two different sequences. Unlike a *substring*, the elements do not need to be contiguous (occupying consecutive positions).

In the context of **Software Engineering**, this is the mathematical foundation for identifying changes between two versions of code, configuration files, or dataset schemas.

---

## 2. The Dynamic Programming Approach

LCS is solved using **Tabulation**, a "bottom-up" Dynamic Programming technique. Instead of re-calculating the same overlaps multiple times (as a recursive solution would), we store the results of smaller comparisons in a 2D matrix.

### 2.1 The Recurrence Relation

For any two sequences  and , the value of the matrix at position `dp[i][j]` is determined as follows:

1. **If the characters match** ():
We have found a common element. We take the result of the previous subproblem and add one.


2. **If the characters do not match** ():
The current LCS is the maximum value found by either ignoring the current character of  or the current character of .



---

## 3. Step-by-Step Matrix Construction

Imagine comparing `ABCD` and `ACBD`:

1. **Initialization:** Create a matrix with an extra row and column of zeros to represent the "empty string" case.
2. **Iteration:** Fill the matrix row by row. If characters match, move diagonally. If they don't, take the max from the top or left.
3. **Completion:** The value at the bottom-right cell (`dp[m][n]`) represents the total length of the Longest Common Subsequence.

---

## 4. Reconstructing the Subsequence (Backtracking)

Once the matrix is filled, we must "walk back" from the end to find the actual characters:

* Start at `dp[m][n]`.
* If the characters of  and  at the current indices match, add the character to our result and move **diagonally** up-left.
* If they do not match, move toward the **larger** of the two neighboring values (up or left).
* Continue until reaching `dp[0][0]`.

---

## 5. Industrial Application: File Diffing

When you run a command like `git diff`, the system is essentially performing an LCS on the lines of your files:

* **Matches:** These are the lines that remain unchanged.
* **Non-Matches (Sequence A):** These are the deletions (`-`).
* **Non-Matches (Sequence B):** These are the additions (`+`).

By identifying the LCS, the tool can minimize the number of changes displayed to the developer, making version history easier to read.

---

## 6. Logic Constraints

* **Order Matters:** The elements must appear in the same order, though not necessarily together.
* **Non-Unique Solutions:** Multiple subsequences of the same maximum length can exist. Our implementation typically picks the one found first during backtracking.