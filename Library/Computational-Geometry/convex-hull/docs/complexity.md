# Convex Hull Complexity Analysis

## 1. Time Complexity

The Monotone Chain algorithm is dominated by the sorting step.

- **Sorting**: $O(N \log N)$, where $N$ is the number of points.
- **Hull Construction**: $O(N)$. Although there is a `while` loop inside the `for` loop, each point is added to the hull exactly once and removed at most once. This is a classic "amortized" linear time complexity.
- **Total Time**: **O(N log N)**.

---

## 2. Space Complexity

- **Storage**: $O(N)$ to store the original points and the resulting hull.
- **Total Space**: **O(N)**.

---

## 3. Comparison with Other Algorithms

| Algorithm | Time Complexity | Notes |
| :--- | :--- | :--- |
| **Monotone Chain** | $O(N \log N)$ | Simple, robust, widely used. |
| **Graham Scan** | $O(N \log N)$ | Uses polar angle sorting; slightly more complex to implement numerically robustly. |
| **QuickHull** | $O(N \log N)$ avg | Similar to QuickSort; can be $O(N^2)$ in worst case. |
| **Chan's Algorithm** | $O(N \log h)$ | "Output-sensitive" (where $h$ is hull size). Theoretical improvement but much harder to implement. |
| **Jarvis March** | $O(Nh)$ | Efficient only if the hull size $h$ is very small. |
