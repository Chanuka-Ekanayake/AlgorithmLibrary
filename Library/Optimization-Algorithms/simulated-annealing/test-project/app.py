import sys
import time
import math
from pathlib import Path

# Add parent directory for core logic
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

try:
    from core.annealer import SimulatedAnnealingOptimizer
except ImportError:
    print("Error: Ensure 'core/annealer.py' and 'core/__init__.py' exist.")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Problem Definition: Travelling Salesman Problem (TSP)
# 10 cities placed in a circle — optimal tour is known to be the perimeter.
# ---------------------------------------------------------------------------

def build_circular_cities(n: int, radius: float = 100.0):
    """
    Place n cities evenly on a circle of the given radius.
    The mathematically optimal TSP tour visits them in order → total
    distance = n × 2r × sin(π/n), which approaches 2πr as n grows.
    """
    cities = []
    for i in range(n):
        angle = 2 * math.pi * i / n
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        cities.append((round(x, 4), round(y, 4)))
    return cities


def run_tsp_demo():
    print("=" * 65)
    print("SYSTEM: ROUTE OPTIMISATION ENGINE")
    print("ALGORITHM: SIMULATED ANNEALING  |  PROBLEM: TSP")
    print("=" * 65 + "\n")

    # -----------------------------------------------------------------------
    # 1. Build a 10-city circular layout
    # -----------------------------------------------------------------------
    NUM_CITIES = 10
    RADIUS = 100.0
    cities = build_circular_cities(NUM_CITIES, RADIUS)

    # Optimal tour = visiting cities in index order (0,1,2,...,9)
    optimal_tour_cost = SimulatedAnnealingOptimizer.tsp_cost(cities)

    print(f"[PROBLEM] {NUM_CITIES} cities on a circle of radius {RADIUS}")
    print(f"[PROBLEM] Mathematically optimal tour distance: {optimal_tour_cost:.4f}\n")

    # -----------------------------------------------------------------------
    # 2. Shuffle the cities to create a bad initial tour
    # -----------------------------------------------------------------------
    import random
    rng = random.Random(42)
    initial_tour = list(cities)
    rng.shuffle(initial_tour)
    initial_cost = SimulatedAnnealingOptimizer.tsp_cost(initial_tour)

    print(f"[INIT]    Shuffled (random) tour distance:  {initial_cost:.4f}")
    print(f"[INIT]    Gap from optimal:                 {initial_cost - optimal_tour_cost:.4f}\n")

    # -----------------------------------------------------------------------
    # 3. Hyperparameters
    # -----------------------------------------------------------------------
    INITIAL_TEMP        = 500.0
    COOLING_RATE        = 0.995
    MIN_TEMP            = 1e-6
    ITERATIONS_PER_TEMP = 200
    SEED                = 99

    print("[HYPERPARAMETERS]")
    print(f"  Initial Temperature  : {INITIAL_TEMP}")
    print(f"  Cooling Rate (α)     : {COOLING_RATE}")
    print(f"  Min Temperature      : {MIN_TEMP}")
    print(f"  Iterations / Temp    : {ITERATIONS_PER_TEMP}")
    print(f"  Random Seed          : {SEED}\n")

    # -----------------------------------------------------------------------
    # 4. Run the Optimiser
    # -----------------------------------------------------------------------
    optimizer = SimulatedAnnealingOptimizer(
        cost_fn              = SimulatedAnnealingOptimizer.tsp_cost,
        neighbour_fn         = SimulatedAnnealingOptimizer.tsp_neighbour,
        initial_temp         = INITIAL_TEMP,
        cooling_rate         = COOLING_RATE,
        min_temp             = MIN_TEMP,
        iterations_per_temp  = ITERATIONS_PER_TEMP,
        seed                 = SEED,
    )

    print("[OPTIMISING] Running Simulated Annealing...")
    start = time.perf_counter()
    best_tour, best_cost, cost_history = optimizer.optimize(initial_tour)
    end = time.perf_counter()

    # -----------------------------------------------------------------------
    # 5. Show cost curve (sampled)
    # -----------------------------------------------------------------------
    print("\n[LOG] Convergence Curve (best cost at temperature checkpoints):")
    total_steps = len(cost_history)
    num_samples = 6
    step = max(total_steps // num_samples, 1)
    sample_steps = list(range(0, total_steps, step))[:num_samples]
    for s in sample_steps:
        print(f"      Step {s+1:<5} | Best Cost: {cost_history[s]:.4f}")

    # -----------------------------------------------------------------------
    # 6. Final Report
    # -----------------------------------------------------------------------
    improvement = ((initial_cost - best_cost) / initial_cost) * 100
    gap_to_optimal = best_cost - optimal_tour_cost

    print("\n" + "=" * 65)
    print("OPTIMISATION REPORT")
    print("=" * 65)
    print(f"  Initial (random) tour cost : {initial_cost:.4f}")
    print(f"  Optimised tour cost        : {best_cost:.4f}")
    print(f"  Known optimal cost         : {optimal_tour_cost:.4f}")
    print(f"  Improvement                : {improvement:.2f}%")
    print(f"  Gap to optimal             : {gap_to_optimal:.4f}")
    print(f"  Temperature steps taken    : {total_steps}")
    print("-" * 65)
    print(f"  Execution Time             : {(end - start) * 1000:.2f} ms")
    print("=" * 65)

    if gap_to_optimal < 1.0:
        print("RESULT: Engine found the optimal or near-optimal global solution.")
    else:
        print("RESULT: Engine significantly improved the route. Try a slower")
        print("        cooling rate (e.g. 0.999) for a tighter optimum.")


if __name__ == "__main__":
    run_tsp_demo()
