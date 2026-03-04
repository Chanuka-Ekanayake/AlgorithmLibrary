# Algorithm Logic: Particle Swarm Optimisation

Particle Swarm Optimisation (PSO) is a **swarm-intelligence metaheuristic** inspired by the emergent collective behaviour observed in bird flocks and fish schools. Introduced by Kennedy & Eberhart in 1995, it is one of the most widely used population-based optimisation algorithms for continuous search spaces.

PSO shines on **non-convex, multimodal objective functions** — surfaces with many local minima — where gradient-based methods like gradient descent cannot escape the first valley they fall into.

---

## 1. The Problem: Multimodal Landscapes

Classical optimisers like gradient descent navigate by following the local slope downward. This is efficient on smooth, bowl-shaped (convex) surfaces, but catastrophic on rugged multimodal landscapes:

- The algorithm immediately descends into the nearest local minimum.
- With no global awareness, it has no mechanism to discover that a much deeper valley exists elsewhere.

PSO addresses this by deploying a **population (swarm) of candidate solutions simultaneously**, each exploring a different region of the search space and sharing what they learn with the group.

---

## 2. Swarm Structure: Particles

The swarm consists of **n particles**. Each particle is characterised by:

| Attribute | Symbol | Description |
|---|---|---|
| Position | **x** | The particle's current point in the search space (a candidate solution) |
| Velocity | **v** | A displacement vector — how far and in what direction the particle will move next |
| Personal Best | **p_best** | The best position this particle has personally visited so far |
| Cost | **f(x)** | The objective function value at the current position |

The swarm also maintains a single shared record:

| Attribute | Symbol | Description |
|---|---|---|
| Global Best | **g_best** | The single best position found by *any* particle across *all* iterations |

---

## 3. The Core Update Equations

### 3.1 Velocity Update

At every iteration, each particle updates its velocity by blending three influences:

$$
v_i(t+1) = \omega \cdot v_i(t) \;+\; c_1 \cdot r_1 \cdot (p\_best_i - x_i(t)) \;+\; c_2 \cdot r_2 \cdot (g\_best - x_i(t))
$$

| Term | Name | Role |
|---|---|---|
| ω · v_i(t) | **Inertia** | Keeps the particle flying in its current direction — momentum |
| c₁ · r₁ · (p_best − x) | **Cognitive component** | Pulls the particle back toward its own historical best position |
| c₂ · r₂ · (g_best − x) | **Social component** | Pulls the particle toward the best position found by the entire swarm |
| r₁, r₂ ∈ [0, 1] | **Stochastic factors** | Freshly sampled each iteration to introduce diversity and prevent premature convergence |

### 3.2 Position Update

After updating velocity, the particle simply moves:

$$
x_i(t+1) = x_i(t) + v_i(t+1)
$$

The new position is then **clamped** to the feasible search bounds to prevent particles from escaping the defined search region.

---

## 4. The Three Hyperparameters

### 4.1 Inertia Weight (ω)

Controls how much of the previous velocity is retained.

- **High ω (> 1.0):** Particles accelerate — wide exploration but risk overshooting.
- **Low ω (< 0.4):** Particles decelerate quickly — tight local search.
- **Commonly used value: ω ≈ 0.729** — motivated by constriction-factor analyses (e.g. Clerc & Kennedy) and often yielding a good exploration–exploitation balance in many benchmark problems; formal convergence guarantees depend on the specific PSO variant and assumptions.

### 4.2 Cognitive Coefficient (c₁)

Controls how strongly a particle is attracted to its own best position.

- High c₁ → individualistic swarm; particles explore independently.
- Low c₁ → particles rely more on the group's wisdom.

### 4.3 Social Coefficient (c₂)

Controls how strongly a particle is attracted to the global best position.

- High c₂ → swarm collapses onto the current global best rapidly (exploitation).
- Low c₂ → swarm stays spread out longer (exploration).

The classical balance: **c₁ = c₂ ≈ 1.494** (from Clerc & Kennedy's constriction coefficient analysis).

---

## 5. Algorithm Pseudocode

```
Initialise swarm:
    for each particle i:
        position[i]  ← random point in bounds
        velocity[i]  ← random small vector
        p_best[i]    ← position[i]

g_best ← position with lowest f(x) across all particles

for t = 1 to max_iterations:
    for each particle i:
        r1, r2 ← uniform random in [0, 1]

        v[i] ← ω · v[i]
              + c₁ · r1 · (p_best[i] − x[i])
              + c₂ · r2 · (g_best     − x[i])

        x[i] ← clamp(x[i] + v[i], bounds)

        if f(x[i]) < f(p_best[i]):
            p_best[i] ← x[i]

        if f(x[i]) < f(g_best):
            g_best ← x[i]

return g_best
```

---

## 6. Why It Works: Collective Intelligence

No single particle follows a gradient. Instead, the swarm achieves intelligent behaviour through **social information sharing**:

1. Early iterations: swarm is spread out, discovering many valleys simultaneously.
2. Mid iterations: particles begin converging toward promising regions, pulled by the shared g_best.
3. Late iterations: swarm clusters around the best-known region and refines it cooperatively.

This mirrors how a flock of birds can collectively locate food faster than any individual bird searching alone.
