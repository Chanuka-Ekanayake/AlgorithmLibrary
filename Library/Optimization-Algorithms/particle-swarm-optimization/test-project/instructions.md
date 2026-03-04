# User Guide: PSO Benchmark Suite (Particle Swarm Optimisation)

This project demonstrates **Particle Swarm Optimisation** minimising three progressively harder mathematical benchmark functions — from a trivial convex bowl all the way to a highly multimodal surface with hundreds of local minima.

## How to Test

1. **Navigate** to the `test-project` folder.
2. **Run** the benchmark suite:
   ```bash
   python app.py
   ```

## What to Experiment With

| Hyperparameter | Location in `app.py` | Effect |
|---|---|---|
| `num_particles` | `run_benchmark(...)` call | More particles → wider global search coverage |
| `max_iterations` | `run_benchmark(...)` call | More iterations → finer convergence |
| `inertia` | `ParticleSwarmOptimizer(...)` | Lower → tighter local search; higher → more momentum |
| `cognitive_coeff` | `ParticleSwarmOptimizer(...)` | Higher → particles trust personal memory more |
| `social_coeff` | `ParticleSwarmOptimizer(...)` | Higher → swarm collapses to global best faster |
| `seed` | `run_benchmark(...)` call | Change to see run-to-run variance |

## Benchmark Difficulty Scale

| Benchmark | Difficulty | Expected Gap to Optimum |
|---|---|---|
| Sphere | ⭐ Easy | < 1e-6 |
| Rosenbrock | ⭐⭐⭐ Medium | < 1.0 |
| Rastrigin | ⭐⭐⭐⭐⭐ Hard | < 5.0 (with defaults) |
