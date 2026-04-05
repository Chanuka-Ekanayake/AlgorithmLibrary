# Complexity Analysis: Ant Colony Optimization

## Time Complexity
The time complexity of ACO for the Traveling Salesman Problem (TSP) depends on the number of cities ($N$), the number of ants ($m$), and the number of iterations ($I$).

1. **Tour Construction:** In each iteration, each of the $m$ ants must select $N$ cities. The selection process evaluates all remaining unvisited cities. 
   - First step: Evaluates $N-1$ cities.
   - Second step: Evaluates $N-2$ cities.
   - Total evaluations per ant is bounded by $O(N^2)$.
   - For $m$ ants, tour construction takes $O(m \cdot N^2)$.
   
2. **Pheromone Update:** After tours are complete, the evaporation phase visits every element in the $N \times N$ matrix, which requires $O(N^2)$ operations. Following that, $m$ ants trace their $N$-step paths and add pheromones taking $O(m \cdot N)$.
   - Total pheromone update taking $O(N^2 + m \cdot N)$.

3. **Overall Time Complexity:**
   The dominant term per iteration is the tour construction. Over $I$ iterations, the total computational complexity becomes:
   **$\mathcal{O}(I \cdot m \cdot N^2)$**

## Space / Auxiliary Complexity
1. **Pheromone Matrix:** Maintains a square matrix connecting every city to every other city: $O(N^2)$.
2. **Distance Matrix:** Maintains a square matrix representing the heuristic / geometric map: $O(N^2)$.
3. **Paths:** Each ant maintains a tour array of size $N$, yielding $O(m \cdot N)$ dynamic memory per iteration.

Overall Space Complexity: **$\mathcal{O}(N^2)$**.

## Scalability and Optimization Methods
While simple ACO scales gracefully up to $N = 1,000$ computationally, performance degrades aggressively if memory bounds hit caching limits. 
In advanced industrial applications, the matrix $O(N^2)$ lookup is commonly sparsified using K-Nearest-Neighbor sub-graphs. In this optimization, an ant at city $i$ does not check all $n-1$ other cities, but rather only the $k$ closest neighboring cities (e.g., $k=15$). This forces the local density check down to $O(k)$ resulting in a practical time complexity constraint closer to $O(I \cdot m \cdot N)$.
