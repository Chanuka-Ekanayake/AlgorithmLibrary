# Complexity Analysis: Genetic Algorithm

Genetic Algorithms are metaheuristics. Their complexity heavily depends on the specific problem being solved, particularly the cost of the **Fitness Function** and the size of the **Chromosome**.

## 1. Time Complexity

The time complexity of a standard Genetic Algorithm over a single run is bounded by:

**O(G × P × (F + S))**

Where:
- **G** = Number of Generations
- **P** = Population Size
- **F** = Time to evaluate the Fitness Function for one individual
- **S** = Size of the Chromosome (length of the genetic array/string)

### Breakdown per Generation:
1. **Fitness Evaluation:** `O(P × F)`. Every individual must be evaluated. In complex problems (like simulating a robot's physics to evaluate its gait), `F` completely dominates the entire algorithm.
2. **Sorting/Elitism:** `O(P log P)`. Sorting the population by fitness to extract the elite.
3. **Selection (Tournament):** `O(P × T)` where `T` is the tournament size. Usually `T` is a small constant (e.g., 3), making this `O(P)`.
4. **Crossover:** `O(P × S)`. Iterating over strings or arrays of length `S` to recombine them.
5. **Mutation:** `O(P × S)`. Iterating over strings or arrays of length `S` to potentially flip genes.

Since `P log P` and `P × S` are usually much smaller than `P × F`, the practical runtime is almost entirely dictated by **O(G × P × F)**.

---

## 2. Space Complexity

The space complexity is bounded by:

**O(P × S)**

Where:
- **P** = Population Size
- **S** = Space required to store one Chromosome in memory.

### Breakdown:
- The algorithm must maintain the current generation of size `P`.
- During the creation of the next generation, a second list of size `P` is built.
- Total memory is roughly `2 × P × S`. 
- Since GAs do not build deep recursive trees (like DFS) or massive matrices (like dynamic programming), their memory footprint is strictly linear and highly predictable.

---

## 3. Performance Trade-offs & Tuning

### The Population Size (P)
- **Small Population:** Fast generations `O(P)`, low memory. High risk of premature convergence (getting stuck in local optima) due to a lack of genetic diversity.
- **Large Population:** Slow generations, high memory. Excellent global search capabilities and high diversity.

### The Mutation Rate
- **Too Low (< 0.001):** The algorithm relies entirely on crossover. Once the population homogenizes, evolution stops.
- **Too High (> 0.1):** The algorithm degrades into a completely Random Search. Good genetic building blocks are destroyed before they can propagate.

### Expected Convergence Time
Unlike exact algorithms (like Dijkstra's or Binary Search), GAs provide **no mathematical guarantee** of finding the absolute global optimum, nor a strict time bound on when they will converge. They are used specifically for NP-Hard problems (like the Traveling Salesman Problem) where an exact O(2^N) algorithm would literally take billions of years, and an "80% optimal solution in 5 seconds" is preferred.
