"""
PSO Benchmark Suite: Multimodal Function Minimisation
======================================================
Demonstrates Particle Swarm Optimisation solving three progressively
harder benchmark functions:

  1. Sphere       — simple convex bowl (sanity check)
  2. Rosenbrock   — curved valley (hard to trace to the minimum)
  3. Rastrigin    — highly multimodal surface with ~100 local minima (stress test)

All three have a known global minimum of 0.0 at the origin (or at (1,...,1)
for Rosenbrock), so we can precisely measure the algorithm's accuracy.
"""

import sys
import time
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

try:
    from core.pso import ParticleSwarmOptimizer
except ImportError:
    print("Error: Ensure 'core/pso.py' and 'core/__init__.py' exist.")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def print_header(title: str) -> None:
    print("\n" + "=" * 65)
    print(f"  {title}")
    print("=" * 65)


def print_section(label: str) -> None:
    print(f"\n[{label}]")


def run_benchmark(
    name: str,
    objective_fn,
    dimensions: int,
    bounds,
    known_optimum: float,
    num_particles: int = 30,
    max_iterations: int = 200,
    seed: int = 42,
) -> None:
    """Run a single benchmark and print a structured report."""
    print_header(f"BENCHMARK: {name.upper()}")

    print_section("PROBLEM")
    print(f"  Dimensions       : {dimensions}")
    if not bounds:
        print("  Search bounds    : <no bounds provided>")
    else:
        first_bound = bounds[0]
        if all(b == first_bound for b in bounds):
            # Uniform bounds across all dimensions; preserve original message style.
            print(f"  Search bounds    : [{first_bound[0]}, {first_bound[1]}] per dimension")
        else:
            # Non-uniform per-dimension bounds; show the full bounds list.
            print(f"  Search bounds    : {bounds}")
    print(f"  Known optimum    : f(x*) = {known_optimum}")
    print(f"  Swarm size       : {num_particles} particles")
    print(f"  Max iterations   : {max_iterations}")

    optimizer = ParticleSwarmOptimizer(
        objective_fn   = objective_fn,
        dimensions     = dimensions,
        bounds         = bounds,
        num_particles  = num_particles,
        max_iterations = max_iterations,
        inertia        = 0.729,
        cognitive_coeff= 1.494,
        social_coeff   = 1.494,
        seed           = seed,
    )

    print_section("OPTIMISING")
    print("  Running PSO swarm...")
    start = time.perf_counter()
    best_pos, best_cost, history = optimizer.optimize()
    elapsed = (time.perf_counter() - start) * 1000

    # Convergence curve (6 sample snapshots)
    print_section("CONVERGENCE LOG")
    total = len(history)
    samples = [int(total * p / 5) for p in range(6)]
    samples[-1] = total - 1
    for s in samples:
        print(f"  Iter {s + 1:<4} | Global Best Cost: {history[s]:.8f}")

    # Final report
    gap = abs(best_cost - known_optimum)
    accuracy_pct = max(0.0, 100.0 - (gap / (abs(known_optimum) + 1e-12)) * 100)

    print_section("RESULT")
    print(f"  Best cost found  : {best_cost:.8f}")
    print(f"  Known optimum    : {known_optimum:.8f}")
    print(f"  Gap to optimum   : {gap:.2e}")
    print(f"  Best position    : [{', '.join(f'{v:.4f}' for v in best_pos[:4])}{'...' if dimensions > 4 else ''}]")
    print(f"  Execution time   : {elapsed:.2f} ms")
    print("-" * 65)

    if gap < 0.01:
        print("  VERDICT: Swarm found the global optimum with high precision.")
    elif gap < 1.0:
        print("  VERDICT: Swarm found a near-optimal solution. Try increasing")
        print("           num_particles or max_iterations for tighter accuracy.")
    else:
        print("  VERDICT: Swarm is in the correct region. This function is")
        print("           highly multimodal — more iterations recommended.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 65)
    print("  SYSTEM: PSO BENCHMARK SUITE")
    print("  ALGORITHM: PARTICLE SWARM OPTIMISATION")
    print("=" * 65)
    print("""
Three canonical benchmark functions test different aspects of PSO:
  1. Sphere     — trivial convex bowl (should reach ~0 immediately)
  2. Rosenbrock — curved banana valley (hard to trace the valley floor)
  3. Rastrigin  — 100s of local minima (true multimodal stress test)
""")

    DIMENSIONS = 10

    # -----------------------------------------------------------------------
    # Benchmark 1: Sphere
    # Simple convex bowl. Global minimum = 0 at origin.
    # PSO should solve this trivially.
    # -----------------------------------------------------------------------
    run_benchmark(
        name          = "Sphere Function",
        objective_fn  = ParticleSwarmOptimizer.sphere,
        dimensions    = DIMENSIONS,
        bounds        = [(-5.12, 5.12)] * DIMENSIONS,
        known_optimum = 0.0,
        num_particles = 30,
        max_iterations= 200,
        seed          = 42,
    )

    # -----------------------------------------------------------------------
    # Benchmark 2: Rosenbrock (Banana Function)
    # Curved valley. Global minimum = 0 at (1, 1, ..., 1).
    # Easy to find the valley; hard to trace it to the minimum precisely.
    # -----------------------------------------------------------------------
    run_benchmark(
        name          = "Rosenbrock (Banana) Function",
        objective_fn  = ParticleSwarmOptimizer.rosenbrock,
        dimensions    = DIMENSIONS,
        bounds        = [(-2.048, 2.048)] * DIMENSIONS,
        known_optimum = 0.0,
        num_particles = 40,
        max_iterations= 500,
        seed          = 42,
    )

    # -----------------------------------------------------------------------
    # Benchmark 3: Rastrigin
    # Highly multimodal. Global minimum = 0 at origin, but surrounded by
    # hundreds of local minima spaced 1.0 apart. The primary PSO stress-test.
    # -----------------------------------------------------------------------
    run_benchmark(
        name          = "Rastrigin Function",
        objective_fn  = ParticleSwarmOptimizer.rastrigin,
        dimensions    = DIMENSIONS,
        bounds        = [(-5.12, 5.12)] * DIMENSIONS,
        known_optimum = 0.0,
        num_particles = 50,
        max_iterations= 500,
        seed          = 42,
    )

    print("\n" + "=" * 65)
    print("  BENCHMARK SUITE COMPLETE")
    print("=" * 65)
    print("""
Tips for improving results on harder functions (Rastrigin):
  - Increase num_particles (try 80-100) for wider swarm coverage
  - Increase max_iterations (try 1000+) for deeper local refinement
  - Lower inertia (try 0.4) to help late-stage convergence
  - Increase max_iterations while lowering inertia linearly over time
    (linear inertia decay: ω decreases from 0.9 → 0.4 over the run)
""")


if __name__ == "__main__":
    main()
