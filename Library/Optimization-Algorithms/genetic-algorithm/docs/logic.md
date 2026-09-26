# Algorithm Logic: Genetic Algorithm (GA)

## 1. Biological Inspiration

The Genetic Algorithm mirrors **Darwinian Evolution**. In nature, individuals in a population compete for resources and survival. The individuals best suited (fittest) to their environment are more likely to survive and reproduce. Their offspring inherit traits (genes) from both parents. Over millions of years, this pressure optimizes the species.

In computer science, we simulate this to solve optimization problems where calculating the absolute perfect answer (brute force) would take longer than the universe has existed (e.g., TSP with 100 cities).

---

## 2. The Four Pillars of the Algorithm

### 2.1 Population & Encoding (Chromosomes)
A **Population** is a collection of candidate solutions. Each solution is called an **Individual** or **Chromosome**. 
- To solve a problem, you must encode a solution into a chromosome. 
- *Example:* If we want to find the maximum of a function $f(x, y)$, a chromosome might be an array `[x, y]`.
- *Example:* If evolving a password guess, a chromosome is a string `"H4x0r"`.

### 2.2 Fitness Function (The Environment)
The **Fitness Function** represents the environment. It takes a chromosome as input and returns a score representing how "good" the solution is. 
- The algorithm's only goal is to maximize (or minimize) this score.
- Designing a smooth, informative fitness function is the most critical part of applying a GA.

### 2.3 Selection (Survival of the Fittest)
We must select parents to breed the next generation. Better fitness should mean a higher chance of selection.
- **Tournament Selection:** Pick $K$ random individuals from the population and select the one with the highest fitness. This is fast, robust, and highly parallelizable.
- **Roulette Wheel Selection:** Assign selection probabilities proportional to fitness. (Prone to premature convergence if one super-individual dominates early).

### 2.4 Reproduction (Crossover & Mutation)
Once two parents are selected, they produce offspring.
- **Crossover (Recombination):** Combine parts of Parent A and Parent B. 
  - *Single-point crossover:* Split both parents at an index, and swap the tails.
- **Mutation:** Randomly alter a tiny fraction of the offspring's genes. 
  - *Why?* Crossover only recombines existing genetic material. Mutation injects *new* material into the gene pool, preventing the algorithm from getting permanently stuck in a local optimum.

---

## 3. The Evolutionary Loop

```text
1. Initialize a random Population of size N.
2. LOOP until max_generations or target_fitness is met:
    a. Evaluate the fitness of everyone in the Population.
    b. (Elitism) Copy the top E individuals directly to the new Population.
    c. WHILE the new Population is smaller than N:
        i.   Select two parents using Tournament Selection.
        ii.  With probability Pc (Crossover Rate), cross them over to make 2 children.
        iii. With probability Pm (Mutation Rate), mutate the children.
        iv.  Add children to the new Population.
    d. Replace the old Population with the new one.
3. Return the individual with the highest fitness ever seen.
```

---

## 4. Addressing Local Optima: Elitism & Diversity

- **Premature Convergence:** If the population quickly becomes identical, crossover does nothing (swapping identical genes yields the same genes). The algorithm is stuck.
- **Mutation** prevents this by maintaining genetic diversity.
- **Elitism** ensures that the "best solution found so far" is never accidentally destroyed by an unlucky mutation or crossover.

## 5. Genetic Algorithm vs. Gradient Descent

| Feature | Gradient Descent | Genetic Algorithm |
| :--- | :--- | :--- |
| **Search Space** | Must be continuous & differentiable | Can be discrete, noisy, or non-differentiable |
| **Locality** | Follows local slopes | Global search (evaluates widely separated areas) |
| **Trap Risk** | Frequently gets stuck in local minima | Resistant to local minima due to population diversity |
| **Speed** | Extremely fast to converge | Computationally heavy and slow |
