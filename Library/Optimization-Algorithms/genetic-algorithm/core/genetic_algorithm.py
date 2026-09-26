"""
Genetic Algorithm (GA) Core Module

A highly generic, metaheuristic optimization engine inspired by natural selection.
It operates on a population of individuals (chromosomes), applying selection,
crossover (recombination), and mutation to iteratively improve the population's
overall fitness over multiple generations.

Author: Algorithm Library
"""

import random
from typing import List, Callable, Any, Tuple


class GeneticAlgorithm:
    """
    A generic Genetic Algorithm engine.
    
    Instead of hardcoding the representation (e.g., bitstrings or arrays),
    this class relies on user-provided functions to define how individuals
    are created, evaluated, crossed over, and mutated.
    """

    def __init__(
        self,
        population_size: int,
        mutation_rate: float,
        crossover_rate: float = 0.9,
        elitism_count: int = 1,
        fitness_func: Callable[[Any], float] = None,
        create_individual_func: Callable[[], Any] = None,
        mutate_func: Callable[[Any, float], Any] = None,
        crossover_func: Callable[[Any, Any], Tuple[Any, Any]] = None,
        maximize_fitness: bool = True,
        tournament_size: int = 3
    ):
        """
        Initialize the GA engine.
        
        Args:
            population_size: Number of individuals in the population.
            mutation_rate: Probability of mutating an individual/gene (passed to mutate_func).
            crossover_rate: Probability that two selected parents will cross over.
            elitism_count: Number of top individuals guaranteed to survive to the next generation.
            fitness_func: Callback taking an individual and returning a float score.
            create_individual_func: Callback returning a single new, random individual.
            mutate_func: Callback taking (individual, mutation_rate) and returning a mutated copy.
            crossover_func: Callback taking (parent1, parent2) and returning (child1, child2).
            maximize_fitness: If True, higher fitness is better. If False, lower is better.
            tournament_size: Number of individuals competing in tournament selection.
        """
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elitism_count = elitism_count
        self.maximize_fitness = maximize_fitness
        self.tournament_size = tournament_size
        
        self.fitness_func = fitness_func
        self.create_individual_func = create_individual_func
        self.mutate_func = mutate_func
        self.crossover_func = crossover_func
        
        self.population: List[Any] = []
        self.generation = 0

    def _initialize_population(self):
        """Creates the initial random population."""
        self.population = [self.create_individual_func() for _ in range(self.population_size)]
        self.generation = 0

    def _sort_by_fitness(self, pop_with_fitness: List[Tuple[Any, float]]) -> List[Tuple[Any, float]]:
        """Sorts the population by fitness in the desired direction."""
        return sorted(pop_with_fitness, key=lambda x: x[1], reverse=self.maximize_fitness)

    def _tournament_selection(self, pop_with_fitness: List[Tuple[Any, float]]) -> Any:
        """
        Selects one parent using tournament selection.
        Picks 'tournament_size' random individuals and returns the best one.
        """
        competitors = random.sample(pop_with_fitness, self.tournament_size)
        best = self._sort_by_fitness(competitors)[0]
        return best[0]

    def evolve_one_generation(self) -> Tuple[Any, float, float]:
        """
        Evolves the population by one generation.
        
        Returns:
            Tuple of (best_individual, best_fitness, average_fitness)
        """
        # 1. Evaluate fitness for all individuals
        pop_with_fitness = [(ind, self.fitness_func(ind)) for ind in self.population]
        pop_with_fitness = self._sort_by_fitness(pop_with_fitness)
        
        # Calculate stats
        best_individual, best_fitness = pop_with_fitness[0]
        avg_fitness = sum(f for _, f in pop_with_fitness) / self.population_size
        
        new_population = []
        
        # 2. Elitism: carry over the absolute best individuals unchanged
        for i in range(self.elitism_count):
            new_population.append(pop_with_fitness[i][0])
            
        # 3. Create the rest of the new generation
        while len(new_population) < self.population_size:
            # Selection
            parent1 = self._tournament_selection(pop_with_fitness)
            parent2 = self._tournament_selection(pop_with_fitness)
            
            # Crossover
            if random.random() < self.crossover_rate:
                child1, child2 = self.crossover_func(parent1, parent2)
            else:
                child1, child2 = parent1, parent2  # Clone
                
            # Mutation
            child1 = self.mutate_func(child1, self.mutation_rate)
            child2 = self.mutate_func(child2, self.mutation_rate)
            
            new_population.append(child1)
            if len(new_population) < self.population_size:
                new_population.append(child2)
                
        self.population = new_population
        self.generation += 1
        
        return best_individual, best_fitness, avg_fitness

    def run(self, max_generations: int, target_fitness: float = None, verbose: bool = False) -> Tuple[Any, float]:
        """
        Runs the algorithm until max_generations is reached or target_fitness is achieved.
        
        Args:
            max_generations: Hard limit on the number of generations.
            target_fitness: Optional early-stopping criteria.
            verbose: If True, prints stats per generation.
            
        Returns:
            Tuple of (absolute_best_individual, its_fitness)
        """
        self._initialize_population()
        
        overall_best = None
        overall_best_fitness = float('-inf') if self.maximize_fitness else float('inf')
        
        for gen in range(1, max_generations + 1):
            best_ind, best_fit, avg_fit = self.evolve_one_generation()
            
            # Update overall best
            if self.maximize_fitness:
                if best_fit > overall_best_fitness:
                    overall_best_fitness = best_fit
                    overall_best = best_ind
            else:
                if best_fit < overall_best_fitness:
                    overall_best_fitness = best_fit
                    overall_best = best_ind
            
            if verbose:
                print(f"Generation {gen:4d} | Best Fit: {best_fit:8.2f} | Avg Fit: {avg_fit:8.2f}")
                
            # Early stopping check
            if target_fitness is not None:
                if (self.maximize_fitness and best_fit >= target_fitness) or \
                   (not self.maximize_fitness and best_fit <= target_fitness):
                    if verbose:
                        print(f"Target fitness reached at generation {gen}.")
                    break
                    
        return overall_best, overall_best_fitness
