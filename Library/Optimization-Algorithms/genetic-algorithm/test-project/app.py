import sys
import io
import time
import random
import string
from pathlib import Path

# Fix Windows console encoding for Unicode output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Add parent directory to path for core logic access
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

try:
    from core.genetic_algorithm import GeneticAlgorithm
except ImportError:
    print("Error: Ensure 'core/genetic_algorithm.py' and 'core/__init__.py' exist.")
    sys.exit(1)


# ============================================================
# PROBLEM DEFINITION: Evolving a Target String
# ============================================================
# The goal is to start with a population of completely random gibberish strings
# and evolve them over generations until one perfectly matches the target string.

TARGET = "ALGORITHM ENGINEERING"
GENES = string.ascii_uppercase + " "

def create_random_string() -> str:
    """Creates a random string of the same length as the target."""
    return "".join(random.choice(GENES) for _ in range(len(TARGET)))

def calculate_fitness(individual: str) -> float:
    """
    Fitness is the number of characters that match the target at the exact position.
    Max fitness = len(TARGET).
    """
    score = 0
    for i, char in enumerate(individual):
        if char == TARGET[i]:
            score += 1
    return float(score)

def crossover(parent1: str, parent2: str) -> tuple:
    """Single-point crossover."""
    if len(parent1) < 2:
        return parent1, parent2
        
    split_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:split_point] + parent2[split_point:]
    child2 = parent2[:split_point] + parent1[split_point:]
    
    return child1, child2

def mutate(individual: str, rate: float) -> str:
    """Randomly replaces characters with a random gene based on the mutation rate."""
    mutated = list(individual)
    for i in range(len(mutated)):
        if random.random() < rate:
            mutated[i] = random.choice(GENES)
    return "".join(mutated)


def run_evolution():
    print("\n" + "=" * 65)
    print("  NATURAL SELECTION SIMULATOR")
    print("  Algorithm: Genetic Algorithm (GA)")
    print("=" * 65)
    print(f"  Target String:    '{TARGET}'")
    print(f"  Max Fitness:      {float(len(TARGET))}")
    print(f"  Chromosome Size:  {len(TARGET)} genes")
    print(f"  Gene Pool:        A-Z and Space")
    print("=" * 65 + "\n")
    
    # Initialize the engine
    ga = GeneticAlgorithm(
        population_size=200,
        mutation_rate=0.02,        # 2% chance per character to mutate
        crossover_rate=0.9,        # 90% chance parents will cross over
        elitism_count=2,           # Keep the top 2 unchanged
        fitness_func=calculate_fitness,
        create_individual_func=create_random_string,
        mutate_func=mutate,
        crossover_func=crossover,
        maximize_fitness=True,
        tournament_size=5
    )
    
    # We will step through generations manually for the visualization effect
    ga._initialize_population()
    
    max_generations = 1000
    target_fitness = float(len(TARGET))
    
    print("Generation | Best Fitness | Best Individual")
    print("-" * 55)
    
    start_time = time.time()
    
    for gen in range(1, max_generations + 1):
        best_ind, best_fit, avg_fit = ga.evolve_one_generation()
        
        # Print progress (throttle a bit so it's visually pleasing)
        if gen % 10 == 0 or best_fit == target_fitness or gen == 1:
            print(f"  {gen:04d}     |    {int(best_fit):02d}/{int(target_fitness):02d}    | {best_ind}")
            time.sleep(0.05)
            
        if best_fit >= target_fitness:
            print("-" * 55)
            print(f"\n[SUCCESS] Target reached in {gen} generations!")
            break
            
    if best_fit < target_fitness:
        print("-" * 55)
        print(f"\n[STOP] Reached max generations ({max_generations}).")
        print(f"Best result: '{best_ind}' (Fitness: {best_fit})")
        
    print(f"Elapsed Time: {time.time() - start_time:.2f} seconds\n")


if __name__ == "__main__":
    run_evolution()
