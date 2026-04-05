import sys
import os
import math
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
project_root_str = str(PROJECT_ROOT)
if project_root_str not in sys.path:
    sys.path.insert(0, project_root_str)

try:
    from core.aco import AntColonyOptimizer
except ImportError as exc:
    raise ImportError(
        f"Unable to import AntColonyOptimizer from 'core.aco'. "
        f"Ensure the project root is available on sys.path: {PROJECT_ROOT}"
    ) from exc
def generate_random_cities(n_cities, seed=42):
    import random
    rng = random.Random(seed)
    return [(rng.uniform(0, 100), rng.uniform(0, 100)) for _ in range(n_cities)]

def compute_distance_matrix(cities):
    n = len(cities)
    matrix = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                dx = cities[i][0] - cities[j][0]
                dy = cities[i][1] - cities[j][1]
                matrix[i][j] = math.sqrt(dx**2 + dy**2)
    return matrix

def main():
    print("=== Ant Colony Optimization for TSP Simulator ===")
    
    n_cities = 20
    print(f"Generating a map with {n_cities} random cities...")
    cities = generate_random_cities(n_cities)
    dist_matrix = compute_distance_matrix(cities)
    
    n_ants = 20
    n_iterations = 100
    print(f"\nInitializing ACO with {n_ants} ants over {n_iterations} iterations.")
    print("Algorithm settings: alpha=1.0 (pheromone), beta=2.0 (heuristic), rho=0.5 (evaporation)")
    
    optimizer = AntColonyOptimizer(
        dist_matrix=dist_matrix,
        n_ants=n_ants,
        n_iterations=n_iterations,
        alpha=1.0,
        beta=2.0,
        evaporation_rate=0.5,
        q=100.0,
        seed=1337
    )
    
    start_time = time.time()
    best_tour, best_length, cost_history = optimizer.optimize()
    elapsed_time = time.time() - start_time
    
    print("\noptimization complete!")
    print(f"Elapsed Time: {elapsed_time:.3f} seconds")
    print(f"Optimal Tour Length Found: {best_length:.2f}")
    
    print("\nCost History (first, middle, last):")
    if cost_history:
        history_len = len(cost_history)
        middle_index = history_len // 2
        last_index = history_len - 1
        print(f"Iteration 0:   {cost_history[0]:.2f}")
        print(f"Iteration {middle_index}:  {cost_history[middle_index]:.2f}")
        print(f"Iteration {last_index}:  {cost_history[last_index]:.2f}")
    else:
        print("No cost history available.")
    
    print("\nBest Tour Structure:")
    tour_str = " -> ".join(map(str, best_tour))
    print(f"{tour_str} -> {best_tour[0]}")

if __name__ == "__main__":
    main()
