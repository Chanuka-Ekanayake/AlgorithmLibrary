"""
Particle Swarm Optimisation (PSO)
Implements the canonical PSO algorithm (Kennedy & Eberhart, 1995) to find
the global minimum of any continuous, differentiable or non-differentiable
objective function in n-dimensional space.

Classic use-case demonstrated: minimising the Rastrigin function — a highly
multimodal benchmark surface with hundreds of local minima.
"""

import math
import random
from typing import Callable, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Type aliases
# ---------------------------------------------------------------------------
Position = List[float]   # A point in the search space
Velocity = List[float]   # A displacement vector


class Particle:
    """
    A single candidate solution that flies through the search space.

    Each particle remembers its own historical best position (cognitive
    memory) and is attracted toward the global best position found by the
    entire swarm (social knowledge).
    """

    def __init__(
        self,
        position: Position,
        velocity: Velocity,
        cost: float,
    ) -> None:
        self.position: Position = list(position)
        self.velocity: Velocity = list(velocity)
        self.cost: float = cost

        # Personal best
        self.best_position: Position = list(position)
        self.best_cost: float = cost

    def update_personal_best(self) -> None:
        """Promote the current position to personal best if it is strictly better."""
        if self.cost < self.best_cost:
            self.best_position = list(self.position)
            self.best_cost = self.cost


class ParticleSwarmOptimizer:
    """
    A swarm-intelligence optimizer inspired by the emergent flocking behaviour
    of birds and schooling of fish (Kennedy & Eberhart, 1995).

    Each particle explores the search space simultaneously, balancing:
      - Inertia   : tendency to keep flying in the current direction
      - Cognition : attraction toward the particle's own historical best
      - Social    : attraction toward the best position found by any particle
    """

    def __init__(
        self,
        objective_fn: Callable[[Position], float],
        dimensions: int,
        bounds: List[Tuple[float, float]],
        num_particles: int = 30,
        max_iterations: int = 200,
        inertia: float = 0.729,
        cognitive_coeff: float = 1.494,
        social_coeff: float = 1.494,
        seed: Optional[int] = None,
    ) -> None:
        """
        Initialise the Particle Swarm Optimiser.

        Args:
            objective_fn:    Function that receives a position (list of floats)
                             and returns a scalar cost (lower is better).
            dimensions:      Number of dimensions in the search space.
            bounds:          Per-dimension search bounds as a list of
                             (min, max) tuples — must have exactly `dimensions`
                             entries.
            num_particles:   Size of the swarm. More particles → better
                             exploration but higher compute per iteration.
            max_iterations:  Total number of velocity/position update cycles.
            inertia:         Weight (ω) applied to the particle's previous
                             velocity — controls momentum. The classic
                             Shi & Eberhart (1998) constriction value is 0.729.
            cognitive_coeff: Weight (c₁) on the personal-best pull.
                             Typical range: [1.4, 2.0].
            social_coeff:    Weight (c₂) on the global-best pull.
                             Typical range: [1.4, 2.0].
            seed:            Optional random seed for reproducible runs.
        """
        if len(bounds) != dimensions:
            raise ValueError(
                f"'bounds' must have exactly {dimensions} entries, "
                f"got {len(bounds)}."
            )

        self.objective_fn = objective_fn
        self.dimensions = dimensions
        self.bounds = bounds
        self.num_particles = num_particles
        self.max_iterations = max_iterations
        self.inertia = inertia
        self.cognitive_coeff = cognitive_coeff
        self.social_coeff = social_coeff
        self._rng = random.Random(seed)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def optimize(self) -> Tuple[Position, float, List[float]]:
        """
        Run the full PSO loop from random initialisation.

        Returns:
            A tuple of:
                - global_best_position : the best position found anywhere
                                         in the search space.
                - global_best_cost     : the objective value at that position.
                - cost_history         : global best cost recorded at the end
                                         of every iteration (for convergence
                                         plots).
        """
        # 1. Initialise swarm
        swarm = self._initialise_swarm()

        # 2. Bootstrap the global best from the initial generation
        global_best_particle = min(swarm, key=lambda p: p.best_cost)
        global_best_position: Position = list(global_best_particle.best_position)
        global_best_cost: float = global_best_particle.best_cost

        cost_history: List[float] = []

        # 3. Main optimisation loop
        for _ in range(self.max_iterations):
            for particle in swarm:
                # 3a. Update velocity
                self._update_velocity(particle, global_best_position)

                # 3b. Move particle and clamp to bounds
                self._update_position(particle)

                # 3c. Evaluate new position
                particle.cost = self.objective_fn(particle.position)

                # 3d. Update personal best
                particle.update_personal_best()

                # 3e. Update global best
                if particle.best_cost < global_best_cost:
                    global_best_cost = particle.best_cost
                    global_best_position = list(particle.best_position)

            cost_history.append(global_best_cost)

        return global_best_position, global_best_cost, cost_history

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _initialise_swarm(self) -> List[Particle]:
        """
        Scatter particles uniformly at random within the search bounds.
        Initial velocities are set to a fraction of the per-dimension range
        to prevent particles from immediately flying out of bounds.
        """
        swarm: List[Particle] = []
        for _ in range(self.num_particles):
            position = [
                self._rng.uniform(lo, hi)
                for (lo, hi) in self.bounds
            ]
            # Velocity initialised in [-(hi-lo)/2, +(hi-lo)/2]
            velocity = [
                self._rng.uniform(-(hi - lo) / 2, (hi - lo) / 2)
                for (lo, hi) in self.bounds
            ]
            cost = self.objective_fn(position)
            swarm.append(Particle(position, velocity, cost))
        return swarm

    def _update_velocity(
        self,
        particle: Particle,
        global_best_position: Position,
    ) -> None:
        """
        Apply the canonical velocity update equation:

            v_i(t+1) = ω · v_i(t)
                     + c₁ · r₁ · (p_best_i − x_i(t))   ← cognitive pull
                     + c₂ · r₂ · (g_best   − x_i(t))   ← social pull

        where r₁, r₂ ∈ [0, 1] are freshly sampled uniform random numbers,
        introducing stochastic diversity into the swarm's movement.
        """
        for d in range(self.dimensions):
            r1 = self._rng.random()
            r2 = self._rng.random()

            inertia_component   = self.inertia * particle.velocity[d]
            cognitive_component = (
                self.cognitive_coeff * r1
                * (particle.best_position[d] - particle.position[d])
            )
            social_component    = (
                self.social_coeff * r2
                * (global_best_position[d] - particle.position[d])
            )

            particle.velocity[d] = (
                inertia_component + cognitive_component + social_component
            )

    def _update_position(self, particle: Particle) -> None:
        """
        Advance the particle by its velocity, then clamp each dimension
        within its bounds to keep the swarm inside the feasible region.

            x_i(t+1) = x_i(t) + v_i(t+1)
        """
        for d in range(self.dimensions):
            particle.position[d] += particle.velocity[d]
            lo, hi = self.bounds[d]
            particle.position[d] = max(lo, min(hi, particle.position[d]))

    # ------------------------------------------------------------------
    # Built-in benchmark functions (usable as objective_fn)
    # ------------------------------------------------------------------

    @staticmethod
    def rastrigin(position: Position) -> float:
        """
        Rastrigin Function — the standard PSO benchmark.

        A highly multimodal surface with a global minimum of 0.0 at the
        origin. Its regular grid of local minima (spaced 1.0 apart) makes
        it an ideal stress-test for swarm exploration.

            f(x) = A·n + Σ [xᵢ² - A·cos(2π·xᵢ)]
            A = 10,  global minimum: f(0,...,0) = 0
        """
        A = 10
        n = len(position)
        return A * n + sum(
            x ** 2 - A * math.cos(2 * math.pi * x)
            for x in position
        )

    @staticmethod
    def sphere(position: Position) -> float:
        """
        Sphere Function — the simplest convex benchmark.

        A smooth bowl with a single global minimum of 0.0 at the origin.
        Used to verify that the swarm converges on a trivially easy surface.

            f(x) = Σ xᵢ²
        """
        return sum(x ** 2 for x in position)

    @staticmethod
    def rosenbrock(position: Position) -> float:
        """
        Rosenbrock (Banana) Function — a curved valley benchmark.

        The global minimum of 0.0 lies inside a narrow, parabolic valley
        at (1, 1, ..., 1). Easy to find the valley, hard to trace it to
        the true minimum — a classic test of convergence precision.

            f(x) = Σ [100·(x_{i+1} − xᵢ²)² + (1 − xᵢ)²]
        """
        total = 0.0
        for i in range(len(position) - 1):
            total += (
                100.0 * (position[i + 1] - position[i] ** 2) ** 2
                + (1.0 - position[i]) ** 2
            )
        return total
