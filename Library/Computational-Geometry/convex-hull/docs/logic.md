# Convex Hull - Monotone Chain Algorithm

## 1. Overview

The **Convex Hull** of a set of points is the smallest convex polygon that contains all the points. A common analogy is to imagine each point as a nail in a board; the convex hull is the shape of a rubber band stretched around all the nails.

The **Monotone Chain Algorithm** (also known as Andrew's Algorithm) is an efficient method for computing the convex hull in $O(N \log N)$ time.

---

## 2. Technical Logic

The algorithm works by splitting the hull into two parts: the **Lower Hull** and the **Upper Hull**.

### Step-by-Step Walkthrough

1.  **Sorting**: Sort all points lexicographically (primarily by $x$-coordinate, secondarily by $y$). This allows us to process the points from left to right.
2.  **Lower Hull Construction**:
    - Iterate through the sorted points.
    - For each point, check if adding it to the current hull creates a "right turn" or makes the points collinear. 
    - We use the **2D Cross Product** to determine the orientation of three points $(O, A, B)$. If $CrossProduct(O, A, B) \leq 0$, it's not a counter-clockwise turn, so we remove the last point from the hull and repeat.
3.  **Upper Hull Construction**:
    - Repeat the process but in reverse order (from right to left).
4.  **Merging**: Combine the lower and upper hulls, ensuring the duplicate start/end points are handled correctly.

---

## 3. Mathematical Tool: Cross Product

The orientation of three points $P_1, P_2, P_3$ is determined by:
$$(x_2 - x_1)(y_3 - y_1) - (y_2 - y_1)(x_3 - x_1)$$

- **Result > 0**: Counter-Clockwise (Left turn)
- **Result < 0**: Clockwise (Right turn)
- **Result = 0**: Collinear
