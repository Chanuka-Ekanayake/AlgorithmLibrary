import sys
import os
import math
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.aco import AntColonyOptimizer

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
    print(f"Iteration 0:   {cost_history[0]:.2f}")
    print(f"Iteration {n_iterations//2}:  {cost_history[n_iterations//2]:.2f}")
    print(f"Iteration {n_iterations-1}:  {cost_history[-1]:.2f}")
    
    print("\nBest Tour Structure:")
    tour_str = " -> ".join(map(str, best_tour))
    print(f"{tour_str} -> {best_tour[0]}")

if __name__ == "__main__":
    main()
