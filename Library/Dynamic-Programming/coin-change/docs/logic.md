# Algorithm Logic: Dynamic Programming Allocation

Dynamic Programming (DP) works by solving a large problem by combining the solutions to smaller, overlapping subproblems. Instead of guessing the right combination of bundles from the top down, we start at $0$ and build our way up to the target, saving the optimal answer at every single step.

## 1. Optimal Substructure (The Core Formula)

The entire algorithm rests on one mathematical truth: **The optimal way to reach a target amount is exactly 1 bundle plus the optimal way to reach the remaining amount.**

Expressed as a recurrence relation:

$$dp[x] = \min_{c \in bundles} (1 + dp[x - c])$$

- $dp[x]$ is the minimum number of bundles needed for amount $x$.
- $c$ is the current bundle denomination we are testing.
- $dp[x - c]$ is the _already calculated_ minimum number of bundles for the remainder.

---

## 2. Bottom-Up Table Construction

Let's trace how the engine calculates the optimal allocation for a target of **6 credits**, using available bundles of **[1, 3, 4]**.

We initialize an array `dp` where the index is the credit amount, and the value is the minimum bundles needed. We start with infinity ($\infty$) for everything except $0$.

_Initial State:_
`dp = [0, ∞, ∞, ∞, ∞, ∞, ∞]`

The engine iterates from 1 to 6. At each step, it looks back at the array to see if adding a specific bundle yields a better total.

**Step 1: Target = 1**

- Try bundle `1`: $1 - 1 = 0$. `dp[0]` is 0. Total = $1 + 0 = 1$.
- Try bundle `3`: Too big.
- Try bundle `4`: Too big.
- _Result:_ `dp[1] = 1`.

**Step 2: Target = 2**

- Try bundle `1`: $2 - 1 = 1$. `dp[1]` is 1. Total = $1 + 1 = 2$.
- _Result:_ `dp[2] = 2`.

**Step 3: Target = 3**

- Try bundle `1`: $3 - 1 = 2$. `dp[2]` is 2. Total = $1 + 2 = 3$.
- Try bundle `3`: $3 - 3 = 0$. `dp[0]` is 0. Total = $1 + 0 = 1$. (New Minimum!)
- _Result:_ `dp[3] = 1`.

**Step 4: Target = 4**

- Try bundle `1`: $1 + dp[3] = 2$.
- Try bundle `3`: $1 + dp[1] = 2$.
- Try bundle `4`: $1 + dp[0] = 1$. (New Minimum!)
- _Result:_ `dp[4] = 1`.

**Step 6 (The Trap): Target = 6**

- Try bundle `1`: $1 + dp[5] = 3$.
- Try bundle `3`: $1 + dp[3] = 1 + 1 = 2$. (New Minimum!)
- Try bundle `4`: $1 + dp[2] = 1 + 2 = 3$.
- _Result:_ `dp[6] = 2`.

Notice what happened at Step 6. A Greedy algorithm would have blindly chosen the `4` bundle, leaving a remainder of 2, resulting in a total of 3 bundles (4 + 1 + 1). The DP engine looked back at `dp[3]` and realized that $3 + 3$ only requires 2 bundles, securing the mathematically optimal choice.

---

## 3. State Tracking: Following the Breadcrumbs

Knowing that we need 2 bundles is useless if we don't know _which_ 2 bundles to allocate to the user's database record.

To solve this, we maintain a `tracker` array alongside the `dp` array. Every time we find a new minimum, we record the exact bundle that got us there.

For our target of 6, the tracker array would end up looking like this:
`tracker = [-1, 1, 1, 3, 4, 1, 3]`

**The Backtracking Phase:**
To generate the final receipt for the user, we start at the target index (6) and walk backward:

1. Look at `tracker[6]`. It says we used bundle **3**.
2. Subtract 3 from our target. Our new target is $6 - 3 = 3$.
3. Look at `tracker[3]`. It says we used bundle **3**.
4. Subtract 3 from our target. Our new target is $3 - 3 = 0$.
5. Target is 0. We are done.

**Final Allocation Receipt:** `[3, 3]`.
