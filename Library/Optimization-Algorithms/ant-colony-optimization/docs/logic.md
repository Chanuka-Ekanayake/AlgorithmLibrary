# Technical Logic: Ant Colony Optimization

## 1. Pheromones and Heuristics

Ant Colony Optimization relies on two discrete sources of information at any state to make decisions:
1. **Pheromone Trails ($\tau_{ij}$)**: The acquired global knowledge from previous iterations. Higher values indicate that previous ants had success traversing edge $(i, j)$.
2. **Heuristic Information ($\eta_{ij}$)**: Local greedy knowledge. Unrelated to past ants, this provides an innate physical bias towards edges that _seem_ good locally. In a TSP, this is typically $\frac{1}{distance_{ij}}$.

## 2. Transition Rule (Edge Selection)

When an ant is situated at city $i$, the probability $P_{ij}$ of transitioning to an unvisited city $j$ is proportional to the combined weight of the pheromone and the heuristic:

$$ P_{ij} = \frac{[\tau_{ij}]^\alpha \cdot [\eta_{ij}]^\beta}{\sum_{unvisited} [\tau_{ik}]^\alpha \cdot [\eta_{ik}]^\beta} $$

- $\alpha$ (Alpha): Influences the reliance on pheromones.
- $\beta$ (Beta): Influences the reliance on purely local distances.

If $\alpha = 0$, ants ignore pheromone information from other ants and select among unvisited cities using only the heuristic term, still as a probabilistic choice weighted by $[\eta_{ij}]^\beta$ (approaching greedy nearest-neighbor behavior as $\beta$ becomes very large).
If $\beta = 0$, ants ignore the distance and rapidly trace the exact same paths other ants found, which leads to highly premature convergence to sub-optimal traps.

## 3. Pheromone Evaporation

Before new pheromones are added by ants after an iteration, a fraction ($\rho$) of all existing pheromones in the global map evaporates:

$$ \tau_{ij} \leftarrow (1 - \rho) \cdot \tau_{ij} $$

This is the algorithm's defense against local minimums. If an edge stops receiving positive reinforcement because it actually belongs to a relatively inefficient route, evaporation removes its influence, allowing ants to discover alternative paths.

## 4. Pheromone Deposit

Once all ants have completed their tours, they deposit new pheromone proportional to the quality of the solution they found:

$$ \Delta \tau_{ij}^k = \frac{Q}{L_k} $$

Where $L_k$ is the total length of the tour found by ant $k$, and $Q$ is an arbitrary constant. The new trail value becomes:

$$ \tau_{ij} \leftarrow \tau_{ij} + \sum_{k=1}^{ants} \Delta \tau_{ij}^k $$

The shorter the path, the larger the deposit on all of its constituent edges.
