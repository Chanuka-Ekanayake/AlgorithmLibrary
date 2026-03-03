"""
Simulated Annealing Optimizer
Implements the Simulated Annealing metaheuristic to escape local minima
and find globally optimal solutions by probabilistically accepting worse
solutions during early high-temperature phases.

Classic use-case demonstrated: Travelling Salesman Problem (TSP).
"""

import math
import random
from typing import Callable, List, Tuple


class SimulatedAnnealingOptimizer:
    """
    A probabilistic optimization engine inspired by the physical annealing
    process in metallurgy — slowly cooling a material to minimise defects.
    """

    def __init__(
        self,
        cost_fn: Callable[[List], float],
        neighbour_fn: Callable[[List], List],
        initial_temp: float = 1000.0,
        cooling_rate: float = 0.995,
        min_temp: float = 1e-8,
        iterations_per_temp: int = 100,
        seed: int | None = None,
    ):
        """
        Initialise the Simulated Annealing engine.

        Args:
            cost_fn:              Function that receives a solution and returns
                                  a scalar cost (lower is better).
            neighbour_fn:         Function that receives a solution and returns
                                  a slightly mutated neighbour solution.
            initial_temp:         Starting temperature — controls exploration width.
            cooling_rate:         Multiplicative factor applied after every
                                  temperature step (0 < rate < 1).
            min_temp:             Algorithm halts when temperature drops below
                                  this threshold.
            iterations_per_temp:  Number of neighbour evaluations at each
                                  temperature level.
            seed:                 Optional random seed for reproducibility.
        """
        self.cost_fn = cost_fn
        self.neighbour_fn = neighbour_fn
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate
        self.min_temp = min_temp
        self.iterations_per_temp = iterations_per_temp
        self._rng = random.Random(seed)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def optimize(
        self, initial_solution: List
    ) -> Tuple[List, float, List[float]]:
        """
        Run the full simulated annealing schedule starting from
        *initial_solution*.

        Args:
            initial_solution: A valid starting candidate solution
                              (e.g. a city-visit order for TSP).

        Returns:
            A tuple of:
                - best_solution  : the globally best solution found.
                - best_cost      : its associated scalar cost.
                - cost_history   : cost of best solution sampled once per
                                   temperature step (for convergence plots).
        """
        current_solution = list(initial_solution)
        current_cost = self.cost_fn(current_solution)

        best_solution = list(current_solution)
        best_cost = current_cost

        temp = self.initial_temp
        cost_history: List[float] = []

        while temp > self.min_temp:
            for _ in range(self.iterations_per_temp):
                # 1. Generate a neighbouring candidate solution
                candidate = self.neighbour_fn(list(current_solution))
                candidate_cost = self.cost_fn(candidate)

                # 2. Compute the energy delta
                delta = candidate_cost - current_cost

                # 3. Always accept improvements; probabilistically accept
                #    worse solutions to escape local minima
                if delta < 0 or self._rng.random() < self._acceptance_probability(delta, temp):
                    current_solution = candidate
                    current_cost = candidate_cost

                    # 4. Track the global best separately
                    if current_cost < best_cost:
                        best_solution = list(current_solution)
                        best_cost = current_cost

            # 5. Record snapshot and cool down
            cost_history.append(best_cost)
            temp *= self.cooling_rate

        return best_solution, best_cost, cost_history

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _acceptance_probability(delta: float, temp: float) -> float:
        """
        Boltzmann acceptance criterion.

        For a cost *increase* of magnitude delta at temperature T,
        the probability of accepting the worse state is e^(-delta/T).

        When T is high this approaches 1.0 (wild exploration).
        When T is near 0 this approaches 0.0 (pure exploitation).
        """
        try:
            return math.exp(-delta / temp)
        except (OverflowError, ZeroDivisionError):
            return 0.0

    # ------------------------------------------------------------------
    # Domain helpers (reusable for TSP-style problems)
    # ------------------------------------------------------------------

    @staticmethod
    def tsp_cost(route: List[Tuple[float, float]]) -> float:
        """
        Euclidean tour length for a list of (x, y) city coordinates.
        The tour is assumed to be a closed loop (last city → first city).
        """
        total = 0.0
        n = len(route)
        for i in range(n):
            x1, y1 = route[i]
            x2, y2 = route[(i + 1) % n]
            total += math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return total

    @staticmethod
    def tsp_neighbour(
        route: List[Tuple[float, float]],
        rng: "random.Random" | None = None,
    ) -> List[Tuple[float, float]]:
        """
        2-opt swap: pick two random positions and reverse the segment
        between them — the gold-standard neighbourhood move for TSP.

        If an RNG is provided, it will be used for sampling to support
        reproducible runs with a seeded optimizer. Otherwise, the global
        module-level random generator is used (backwards compatible).
        """
        n = len(route)
        sampler = rng.sample if rng is not None else random.sample
        i, j = sorted(sampler(range(n), 2))
        route[i:j + 1] = reversed(route[i:j + 1])
        return route
