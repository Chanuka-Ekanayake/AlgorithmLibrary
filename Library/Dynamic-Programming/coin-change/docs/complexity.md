# Complexity Analysis: Dynamic Programming Allocation

The Coin Change algorithm is a classic example of **pseudo-polynomial time**. The performance depends not just on the number of available bundle types, but on the numeric value of the target itself.

## 1. Time Complexity

Let $T$ be the target allocation amount (e.g., 13,450 credits) and $B$ be the number of available bundle denominations.

| Approach                    | Time Complexity     | Explanation                                                                                                 |
| --------------------------- | ------------------- | ----------------------------------------------------------------------------------------------------------- |
| **Greedy Algorithm**        | $O(B \log B)$       | Sorts the bundles, then repeatedly subtracts the largest possible bundle. Very fast, but often incorrect.   |
| **Brute Force (Recursion)** | $O(B^T)$            | Tries every single possible combination of bundles. Will instantly cause a stack-overflow on large targets. |
| **Dynamic Programming**     | **$O(T \times B)$** | Builds the solution iteratively. For every amount from 1 to $T$, it checks all $B$ bundles.                 |

### The $O(T \times B)$ Reality

Because the outer loop runs exactly $T$ times, and the inner loop runs exactly $B$ times, the time complexity is linear relative to the target amount.
If a user requests 1,000,000 API credits, and you have 5 bundle types, the DP engine will execute exactly 5,000,000 operations. For modern CPUs, this is processed in a fraction of a second, making it perfectly viable for live checkout computations.

---

## 2. Space Complexity

| Structure               | Space Required | Description                                                                                |
| ----------------------- | -------------- | ------------------------------------------------------------------------------------------ |
| **DP Minimums Array**   | $O(T)$         | An array of size $T + 1$ storing the minimum bundles needed for every intermediate amount. |
| **State Tracker Array** | $O(T)$         | An array of size $T + 1$ storing the specific bundle used to reach that amount.            |
| **Total Space**         | **$O(T)$**     | The memory footprint scales linearly with the target amount.                               |

If $T$ is 1,000,000, the arrays require allocating 2,000,000 integers. In Python, this consumes roughly 16 MB of RAM. While this is slightly heavier than a Greedy algorithm's $O(1)$ space, the guarantee of an optimal allocation easily justifies the memory footprint.

---

## 3. The "Greedy Fallacy"

Why can't we just use a Greedy algorithm? A greedy approach always picks the largest possible bundle first. This works perfectly for standard US currency (quarters, dimes, nickels, pennies).

However, in an e-commerce platform where you define custom pricing tiers, a Greedy algorithm will fail catastrophically.

**The Scenario:**

- **Available Credit Bundles:** `[1, 15, 25]`
- **User Target Amount:** `30` credits

**The Greedy Attempt:**

1. Pick the largest bundle: `25`. (Remaining: 5)
2. `15` is too big.
3. Pick `1` five times to finish. (Remaining: 0)

- **Greedy Result:** `[25, 1, 1, 1, 1, 1]` -> **6 bundles used.**

**The Dynamic Programming Reality:**
The DP engine evaluates all overlapping subproblems and realizes that reaching 15 optimally takes 1 bundle. Therefore, reaching 30 optimally takes $15 + 15$.

- **DP Result:** `[15, 15]` -> **2 bundles used.**

If your database charges computational overhead per bundle allocated, or if these bundles represent physical server instances, the Greedy algorithm just cost you 300% more resources than the mathematically optimal DP solution.
