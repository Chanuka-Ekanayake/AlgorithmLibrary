# Complexity Analysis: Matrix Chain Multiplication

## Time Complexity

The time complexity of the dynamic programming solution for Matrix Chain Multiplication is **$O(n^3)$**, where $n$ is the number of matrices in the chain.

**Derivation:**
- The algorithm uses a 2D table `dp` of size $(n+1) \times (n+1)$ to store the minimum costs.
- There are $O(n^2)$ subproblems to solve (one for each possible chain length $L$ and starting index $i$).
- For each subproblem of length $L$, we need to try $L-1$ possible split points $k$. In the worst case, this takes $O(n)$ time.
- Therefore, the total time to compute all entries in the table is bounded by $n \times n \times n = O(n^3)$.

This is a significant improvement over the naive recursive approach, which tests every possible parenthesization and takes exponential time $\Omega(4^n / n^{3/2})$.

## Space Complexity

The space complexity of the algorithm is **$O(n^2)$**.

**Derivation:**
- We maintain two 2D arrays:
  - `dp[0..n][0..n]` to store the optimal scalar multiplication costs.
  - `split[0..n][0..n]` to store the optimal split points to reconstruct the solution.
- Each table takes $O(n^2)$ memory space.
- The depth of the recursion tree when reconstructing the final parenthesization string is $O(n)$, which uses $O(n)$ auxiliary stack space.
- Overall space complexity is dominated by the 2D arrays, yielding $O(n^2)$.
