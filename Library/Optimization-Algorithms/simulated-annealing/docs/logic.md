# Algorithm Logic: Simulated Annealing

Simulated Annealing (SA) is a **probabilistic metaheuristic** inspired by the physical process used in metallurgy where a material is heated to a high temperature and then slowly cooled to reduce structural defects and reach a low-energy crystalline state.

The algorithm is especially powerful for **combinatorial optimisation problems** (like the Travelling Salesman Problem) where the solution space is enormous, highly non-convex, and dotted with countless local minima that trap greedy algorithms.

---

## 1. The Problem: Local Minima Traps

Greedy optimisers (like Hill Climbing) always move to a better neighbour. This sounds sensible, but it means the algorithm gets permanently stuck the moment it reaches a local minimum — a solution that is better than all its immediate neighbours but is **not** the global best.

Simulated Annealing escapes this by introducing a controlled element of randomness: it occasionally **accepts a worse solution** on purpose, allowing it to climb out of a local valley and explore other, potentially deeper valleys.

---

## 2. The Core Concept: Temperature

The algorithm maintains a single scalar value called **Temperature (T)**, which starts high and is gradually reduced according to a **cooling schedule**.

- **High Temperature:** The algorithm is exploratory. Even solutions that are significantly *worse* have a meaningful probability of being accepted. The system wanders broadly across the solution landscape.
- **Low Temperature:** The algorithm becomes increasingly exploitative. Worse solutions are almost never accepted. The system settles into the best region it has found and refines it like a classical hill-climber.

---

## 3. The Acceptance Criterion: Boltzmann Probability

At every iteration, a candidate neighbour is generated. If the candidate is *better*, it is always accepted. If it is *worse* (positive energy delta `Δ`), it is accepted with the **Boltzmann probability**:

$$
P(\text{accept}) = e^{-\Delta / T}
$$

Where:
- **Δ** = `candidate_cost − current_cost` (always positive for a worse solution)
- **T** = current temperature

### Intuition

| Scenario | Effect on Probability |
|---|---|
| T is very large | `−Δ/T ≈ 0`, so `P ≈ e⁰ = 1.0` | Almost always accept |
| T is very small | `−Δ/T → −∞`, so `P ≈ 0.0` | Almost never accept |
| Δ is small | A slightly worse solution has high P | Easy to escape shallow traps |
| Δ is large | A drastically worse solution has low P | Wild jumps still filtered |

---

## 4. The Cooling Schedule

After every temperature level, the temperature is reduced by a multiplicative factor called the **Cooling Rate (α)**:

$$
T_{\text{new}} = \alpha \times T_{\text{current}} \quad \text{where } 0 < \alpha < 1
$$

This is called **geometric (exponential) cooling** and is the most widely used schedule in practice. The algorithm terminates once T drops below a minimum threshold (`min_temp`).

| Cooling Rate | Characteristic |
|---|---|
| `α ≈ 0.999` | Very slow cooling — high quality but expensive |
| `α ≈ 0.995` | Balanced — good quality at reasonable speed |
| `α ≈ 0.90`  | Fast cooling — quick but risks premature convergence |

---

## 5. The Neighbourhood Function (TSP: 2-opt Swap)

A neighbourhood function defines what a "small change" looks like for a given solution representation. For the **Travelling Salesman Problem**, the industry-standard move is the **2-opt swap**:

1. Pick two random indices `i` and `j` in the city tour.
2. Reverse the segment of cities between `i` and `j`.
3. This reconnects the tour in a way that eliminates one crossing, which almost always reduces the total distance.

---

## 6. Algorithm Pseudocode

```
current  ← initial_solution
best     ← current
T        ← initial_temp

while T > min_temp:
    for _ in range(iterations_per_temp):
        candidate ← neighbour(current)
        Δ         ← cost(candidate) − cost(current)

        if Δ < 0 or random() < exp(−Δ / T):
            current ← candidate
            if cost(current) < cost(best):
                best ← current

    T ← cooling_rate × T

return best
```
