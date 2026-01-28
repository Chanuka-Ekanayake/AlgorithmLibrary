# Algorithm Logic: 0/1 Knapsack Problem

## 1. The Problem Definition

The **0/1 Knapsack Problem** is a combinatorial optimization challenge. Given a set of items, each with a **weight** and a **value**, the goal is to determine the number of each item to include in a collection so that the total weight is less than or equal to a given limit and the total value is as large as possible.

The "**0/1**" indicates that you cannot break items (you take the whole item or nothing), making it significantly more difficult than the *Fractional Knapsack* problem.

---

## 2. The Dynamic Programming Strategy

This algorithm uses **Tabulation** to build a global solution from optimal subproblems. We create a 2D matrix where:

* **Rows ():** Represent the items considered so far.
* **Columns ():** Represent the incremental capacity of the knapsack from 0 to .

### 2.1 The Decision Matrix

For every cell in the table `dp[i][w]`, we make a binary choice:

1. **Exclude Item :** If the item is too heavy for the current capacity , or if including it yields a lower total value than the previous optimal solution, we carry forward the value from the cell directly above:


2. **Include Item :** If the item fits, we compare the value of excluding it against the value of including it (Item Value + optimal value for the remaining capacity):



---

## 3. Step-by-Step Execution

1. **Initialize:** Create the  matrix filled with zeros.
2. **Iterate:** Fill the matrix row by row. Each cell represents the "best we can do" given  items and  weight.
3. **Result:** The value in the final cell `dp[N][W]` is the maximum possible value.
4. **Backtrack:** To find the actual items used, compare `dp[i][w]` with `dp[i-1][w]`. If they differ, item  was included.

---

## 4. Engineering Application: Server Resource Optimization

In your software marketplace, the Knapsack logic is used for **Optimal Resource Allocation**:

* **The "Knapsack":** A cloud server with a fixed amount of VRAM (e.g., 24GB).
* **The "Items":** Different ML models, each requiring specific VRAM (weight) and providing specific utility/revenue (value).
* **The Goal:** Choose the combination of models that generates the highest revenue without exceeding the server's VRAM.

---

## 5. Why Tabulation over Recursion?

A naive recursive approach has a time complexity of  because it re-calculates the same weight/item combinations repeatedly. Tabulation ensures each sub-state is calculated exactly once, transforming an exponential problem into a manageable  one.