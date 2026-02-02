# Complexity Analysis: 0/1 Knapsack Problem

The 0/1 Knapsack Problem is a classic example of a problem that is **NP-complete**. However, using Dynamic Programming (Tabulation), we can achieve a solution that is efficient enough for most practical engineering applications.

## 1. Time Complexity

The time complexity of the tabulation approach is:


### 1.1 Parameter Breakdown

* **:** The number of items available to choose from.
* **:** The total capacity of the knapsack (e.g., maximum weight, budget, or VRAM).

### 1.2 Justification

The algorithm builds a 2D matrix of size .

1. **Table Filling:** We iterate through every cell in the matrix exactly once. For each cell, we perform a constant time  comparison to decide whether to include the current item.
2. **Backtracking:** To identify which specific items were selected, we traverse back through the matrix. This takes  steps.

**Total Time:** , which simplifies to .

---

## 2. Space Complexity

The space complexity is:


### 2.1 Memory Usage

The primary space requirement is the 2D array used for tabulation.

* For 100 items () and a capacity of 1,000 (), the matrix stores 100,000 integers.
* **Scaling Issue:** Unlike algorithms that scale only with input size, Knapsack scales with the **magnitude** of the capacity. If  is a very large number (e.g., ), the memory requirements will exceed standard system limits.

### 2.2 Optimization (Space-Efficient DP)

If only the **maximum value** is needed (and not the specific items), space complexity can be reduced to  by only keeping the current and previous rows of the matrix.

---

## 3. The "Pseudo-Polynomial" Concept

While  looks like polynomial time, it is technically **pseudo-polynomial**.

* The complexity depends on the numeric value of , not just the number of bits required to represent .
* If  grows exponentially relative to the number of items, the algorithm effectively behaves like an exponential-time algorithm.

---

## 4. Comparison of Approaches

| Approach | Time Complexity | Space Complexity | Result Type |
| --- | --- | --- | --- |
| **Brute Force (Recursive)** |  |  | Optimal |
| **DP (Tabulation)** |  |  | Optimal |
| **Greedy (Fractional)** |  |  | Non-Optimal for 0/1 |

---

## 5. Performance Summary

| Metric | Complexity |
| --- | --- |
| **Average Time** |  |
| **Worst-Case Time** |  |
| **Auxiliary Space** |  |
| **Optimization Method** | Dynamic Programming (Bottom-Up) |