# Matrix Chain Multiplication Logic

The Matrix Chain Multiplication problem is an optimization problem that can be solved using Dynamic Programming. The goal is to find the most efficient way to multiply a given sequence of matrices. The problem is not actually to *perform* the multiplications, but merely to decide the sequence of the matrix multiplications involved.

## Optimal Substructure

A subproblem of finding the best way to multiply matrices $A_i \dots A_j$ (where $i \le j$) can be divided into two smaller subproblems:
1. Multiply the sequence of matrices $A_i \dots A_k$
2. Multiply the sequence of matrices $A_{k+1} \dots A_j$
...and then multiply the two resulting matrices together.

For the overall sequence to be optimally parenthesized, the sub-sequences $A_i \dots A_k$ and $A_{k+1} \dots A_j$ must also be optimally parenthesized. This optimal substructure allows us to use dynamic programming.

## Recurrence Relation

Let $m[i,j]$ be the minimum number of scalar multiplications needed to compute the matrix $A_{i..j}$ (for $1 \le i \le j \le n$). Let the dimension of matrix $A_m$ be $p_{m-1} \times p_m$.

- If $i = j$, the chain consists of just one matrix $A_i$, so no scalar multiplications are needed:
  $$m[i,i] = 0$$

- If $i < j$, we can split the product at any matrix $k$ ($i \le k < j$). The cost of multiplying the chain $A_i \dots A_j$ optimally by splitting at $k$ is:
  $$m[i,j] = \min_{i \le k < j} \left( m[i,k] + m[k+1,j] + p_{i-1} \cdot p_k \cdot p_j \right)$$

This recurrence naturally leads to a bottom-up dynamic programming approach where we first solve paths of length 1, then length 2, up to length $n$.
