# Monte Carlo Simulation Complexity Analysis

When analyzing the complexity of a Monte Carlo Simulation, the metrics significantly differ from traditional deterministic algorithms. Rather than just focusing on pure operational Time Complexity, we must rigorously analyze the **Error Convergence Rate** (how accuracy improves with computational time) and **Parallelizability**.

Let $N$ be the number of random independent samples (or "simulations") drawn.

---

## 1. Time Complexity

The time complexity of a standard Monte Carlo simulation scales linearly with the number of samples you choose to generate.

$$ \text{Time Complexity} = \mathcal{O}(N \times C) $$

Where:
- $N$ = The number of random samples/paths/darts.
- $C$ = The computational cost of evaluating a *single* sample.

### Examples based on implementation:
1. **Estimating $\pi$:** $C$ is $\mathcal{O}(1)$ because checking if $x^2 + y^2 < 1$ is a single floating-point math operation. Overall time complexity: **$\mathcal{O}(N)$**.
2. **1D Random Walk:** $C$ depends on the number of discrete steps $S$ taken in the walk. Overall time complexity: **$\mathcal{O}(N \times S)$**.
3. **Geometric Brownian Motion (Financial Pricing):** $C$ depends on the number of trading time increments (e.g., $T$ days). Generating random Gaussian shocks and calculating logarithmic returns for each day implies a cost of $T$. Overall time complexity: **$\mathcal{O}(N \times T)$**.

Because Monte Carlo requires heavily massive sample sizes ($N > 10^5$) to be accurate, optimizing the inner loop code (the $C$ factor) via vectorization (NumPy) or lower-level languages (C++/CUDA) is absolutely vital in production.

---

## 2. Space / Memory Complexity

The defining trait of basic Monte Carlo simulations is that independent samples usually do not need to "talk" to each other or be stored indefinitely.

$$ \text{Space Complexity} = \mathcal{O}(1) \text{ auxiliary space} $$

*If memory is managed strictly as a running total:*
- **Estimating $\pi$:** We only maintain an integer `points_inside_circle` and a loop counter. Space is **$\mathcal{O}(1)$**.
- **Average Path Evaluation:** When pricing an option using GBM, we only need to keep a running sum of final prices `sum_p += final_price`. Space is **$\mathcal{O}(1)$**.

*If storing historical paths:*
- Sometimes, analysts need to plot every path or calculate path-dependent statistics (like Asian or Lookback options). In this scenario, we must store arrays of data. Space complexity becomes **$\mathcal{O}(N \times S)$**.

---

## 3. The Error Convergence Rate (Accuracy vs Computational Cost)

The absolute theoretical bottleneck of Monte Carlo methods is the **slow rate of convergence**.

According to the Central Limit Theorem, the standard error $\epsilon$ of the estimate is inversely proportional to the square root of the number of samples $N$:

$$ \text{Error } \epsilon \propto \frac{1}{\sqrt{N}} $$

### The "Factor of 100" Penalty
Because of the $\frac{1}{\sqrt{N}}$ relationship, gaining an extra decimal place of accuracy (reducing the error by a factor of $10$) requires scaling the computations by a factor of $10^2 = 100$.
- To reduce error by 10x $\rightarrow$ do 100x more computing.
- To reduce error by 100x $\rightarrow$ do 10,000x more computing.

This demonstrates that brute-force Monte Carlo is computationally expensive when highly precise deterministic accuracy is required.

---

## 4. Comparing Algorithms: The Curse of Dimensionality

Why bother with Monte Carlo if its error converges so slowly compared to deterministic methods? The answer lies in multi-dimensional problems.

Imagine trying to calculate the volume (integral) of a 10-dimensional sphere.

### Deterministic Grid Integration (e.g., Riemann Sums, Simpson's Rule)
- For 1 dimension, if you slice the line into $M$ grids, the error is bounded by $\mathcal{O}(M^{-2})$.
- For $D$ dimensions, you must lay down a grid of $M^D$ points.
- The error rate of a deterministic grid essentially scales as $\mathcal{O}(N^{-2 / D})$.
- In 10 dimensions, the error drops at an agonizingly slow rate of $\mathcal{O}(N^{-0.2})$. It takes astronomical computational power to calculate.

### Monte Carlo Integration
- The Monte Carlo error relies *only* on the variance of the samples and $N$.
- The Monte Carlo error rate is strictly: $\mathcal{O}(N^{-0.5})$.
- **Crucially: The error rate is completely independent of the number of dimensions $D$.**

For numerical problems in highly complex multi-dimensional probability spaces (like pricing financial derivatives with 50 underlying variables, or complex quantum mechanics models), Monte Carlo is often the *only* mathematically feasible approach.

---

## 5. Parallelizability

Monte Carlo Methods are famously described as **"Embarrassingly Parallel"**.
Because sample $X_1$ contains absolutely no dependency on sample $X_2$, the algorithm can be trivially split across multiple CPU cores, clusters of machines, or GPU threads.

- **Speedup:** Near perfect linear scaling. Running on 10,000 GPU cores computes $10,000\times$ faster than a single core. The only bottleneck is the final aggregation (sum/reduce) phase.

## 6. Summary Table

| Metric | Complexity | Notes |
| :--- | :--- | :--- |
| Time Complexity | $\mathcal{O}(N \times C)$ | Linear w.r.t number of samples $N$. |
| Space Complexity| $\mathcal{O}(1)$ | Often constant unless saving full paths. |
| Error Rate | $\mathcal{O}(\frac{1}{\sqrt{N}})$| Requires 100x compute for 10x accuracy. |
| Multi-Dimensional Scaling | Excellent | Unaffected by the Curse of Dimensionality. |
| Parallelization | Perfect | Embarrassingly parallelizable (GPUs). |