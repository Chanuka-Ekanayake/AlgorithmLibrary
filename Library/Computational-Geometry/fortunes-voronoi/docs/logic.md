# Fortune's Algorithm: Logic and Mathematical Foundation

This document details the mathematical logic behind the $O(N \log N)$ Fortune's sweep-line algorithm for constructing Voronoi Diagrams.

## 1. Geometric Concepts

### 1.1 Voronoi Diagrams
Given a set of sites $S = \{p_1, p_2, \dots, p_n\}$ in a 2D plane, the Voronoi Cell $V(p_i)$ for site $p_i$ is the set of all points closer to $p_i$ than to any other site in $S$:
$$V(p_i) = \{ x \in \mathbb{R}^2 \mid d(x, p_i) \le d(x, p_j) \;\; \forall j \neq i \}$$

### 1.2 The Beach Line
A horizontal line $L$ sweeps down from $y = +\infty$ to $y = -\infty$. 
For any site $p_i = (x_i, y_i)$ above the sweep line $L$ ($y_i > L$), the locus of points equidistant from $p_i$ and $L$ is a parabola:
$$y = f_i(x) = \frac{(x - x_i)^2}{2(y_i - L)} + \frac{y_i + L}{2}$$

The **beach line** is the lower envelope of these parabolas. It consists of multiple parabolic arcs joined at **breakpoints**.

### 1.3 Breakpoints
A breakpoint is the intersection of two adjacent parabolic arcs on the beach line. A breakpoint between the arc of site $p_1 = (x_1, y_1)$ and $p_2 = (x_2, y_2)$ is equidistant from $p_1$, $p_2$, and the sweep line $L$. As the sweep line moves, breakpoints trace out the Voronoi edges.

---

## 2. Event Types & Processing

### 2.1 Site Events
A site event occurs when the sweep line $L$ passes through a site $P = (x_p, y_p)$.
- A new parabolic arc is inserted into the beach line.
- The arc directly above $x_p$ is split into two parts: $A \to A \leftrightarrow B \leftrightarrow A$.
- Two new half-edges are initialized, starting at the point $(x_p, f_A(x_p))$.

### 2.2 Circle Events
A circle event occurs when three adjacent arcs (associated with sites $p_A, p_B, p_C$) converge to a single point.
- This convergence happens when the sweep line reaches the lowest point of the circle circumscribing $p_A$, $p_B$, and $p_C$.
- The circumcenter $V$ of the three sites represents a Voronoi vertex.
- The middle arc $p_B$ disappears from the beach line.
- The two edges separating $p_A, p_B$ and $p_B, p_C$ meet at $V$ and terminate.
- A new edge separating $p_A$ and $p_C$ begins at $V$.

---

## 3. Mathematical Calculations

### 3.1 Breakpoint Calculation
To find the intersection of the parabolas for $p_1$ and $p_2$, we set $f_1(x) = f_2(x)$:
$$\frac{(x-x_1)^2 + y_1^2 - L^2}{2(y_1 - L)} = \frac{(x-x_2)^2 + y_2^2 - L^2}{2(y_2 - L)}$$

Letting $a_1 = \frac{1}{y_1-L}$ and $a_2 = \frac{1}{y_2-L}$, this reduces to the quadratic equation:
$$A x^2 + B x + C = 0$$
where:
- $A = a_1 - a_2$
- $B = -2(x_1 a_1 - x_2 a_2)$
- $C = a_1 x_1^2 - a_2 x_2^2 + y_1 - y_2$

Roots are computed via the quadratic formula. The correct root is selected based on the relative height of the sites:
- If $y_1 > y_2$, we choose the smaller root.
- If $y_1 < y_2$, we choose the larger root.
- If $y_1 = y_2$, the intersection is linear at $x = \frac{x_1 + x_2}{2}$.

### 3.2 Circumcircle Calculation
The circumcenter $(u_x, u_y)$ of points $p_A, p_B, p_C$ is found using determinants:
$$d = 2 \cdot (x_a(y_b - y_c) + x_b(y_c - y_a) + x_c(y_a - y_b))$$
$$u_x = \frac{(x_a^2 + y_a^2)(y_b - y_c) + (x_b^2 + y_b^2)(y_c - y_a) + (x_c^2 + y_c^2)(y_a - y_b)}{d}$$
$$u_y = \frac{(x_a^2 + y_a^2)(x_c - x_b) + (x_b^2 + y_b^2)(x_a - x_c) + (x_c^2 + y_c^2)(x_b - x_a)}{d}$$
$$R = \sqrt{(x_a - u_x)^2 + (y_a - u_y)^2}$$

The circle event is scheduled at $y = u_y - R$.
