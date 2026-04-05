class AntColonyOptimizer:
    """
    Ant Colony Optimization (ACO) algorithm for solving the Traveling Salesman Problem (TSP).
    This implementation uses a pure Python approach without external dependencies.
    """
    def __init__(self, dist_matrix, n_ants=10, n_iterations=100, alpha=1.0, beta=2.0, evaporation_rate=0.5, q=100.0, seed=None):
        """
        Initializes the Ant Colony Optimizer.

        Args:
            dist_matrix (list of list of floats): A 2D square matrix representing the distances between cities.
            n_ants (int): Number of ants used per iteration.
            n_iterations (int): Total number of iterations to run.
            alpha (float): Power parameter for the pheromone. Determines importance of pheromone.
            beta (float): Power parameter for the heuristic (visibility). Determines importance of distance.
            evaporation_rate (float): Rate at which pheromone evaporates (between 0 and 1).
            q (float): Pheromone deposit factor. Total pheromone deposited by an ant on a tour is Q/tour_length.
            seed (int): Optional random seed for reproducibility.
        """
        import random
        self.dist_matrix = dist_matrix
        self.n_cities = len(dist_matrix)
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.q = q
        self.rng = random.Random(seed)
        
        # Initialize pheromone matrix with small positive values (1.0)
        self.pheromones = [[1.0 for _ in range(self.n_cities)] for _ in range(self.n_cities)]

    def optimize(self):
        """
        Runs the ACO algorithm to find the shortest TSP tour.

        Returns:
            tuple: (best_tour (list), best_tour_length (float), history_best_cost (list))
        """
        global_best_tour = None
        global_best_length = float('inf')
        cost_history = []

        for iteration in range(self.n_iterations):
            all_tours = []
            
            # Step 1: Construct ant solutions
            for ant in range(self.n_ants):
                tour, tour_length = self._construct_tour()
                all_tours.append((tour, tour_length))
                
                # Check for global best
                if tour_length < global_best_length:
                    global_best_length = tour_length
                    global_best_tour = tour

            # Step 2: Global pheromone update
            self._update_pheromones(all_tours)
            
            # Record history
            cost_history.append(global_best_length)

        return global_best_tour, global_best_length, cost_history

    def _construct_tour(self):
        """
        Constructs a valid TSP tour for a single ant.
        """
        start_city = self.rng.randint(0, self.n_cities - 1)
        tour = [start_city]
        visited = set([start_city])
        tour_length = 0.0

        current_city = start_city
        for _ in range(self.n_cities - 1):
            next_city = self._select_next_city(current_city, visited)
            tour.append(next_city)
            tour_length += self.dist_matrix[current_city][next_city]
            visited.add(next_city)
            current_city = next_city
            
        # Complete the tour by returning to the start city
        tour_length += self.dist_matrix[current_city][start_city]
        
        return tour, tour_length

    def _select_next_city(self, current_city, visited):
        """
        Selects the next city to visit using the transition probability rule.
        """
        probabilities = []
        unvisited_cities = [c for c in range(self.n_cities) if c not in visited]
        
        for city in unvisited_cities:
            # Pheromone level
            tau = self.pheromones[current_city][city] ** self.alpha
            
            # Heuristic value (visibility is inverse of distance)
            distance = self.dist_matrix[current_city][city]
            # Avoid division by zero
            visibility = 1.0 / distance if distance > 0 else float('inf')
            eta = visibility ** self.beta
            
            probabilities.append(tau * eta)
            
        # Normalize probabilities
        total_prob = sum(probabilities)
        if total_prob == 0:
            # If all probabilities are 0 due to 0 pheromones (unlikely but safe), pick uniformly
            return self.rng.choice(unvisited_cities)
            
        probabilities = [p / total_prob for p in probabilities]
        
        # Roulette wheel selection based on calculated probabilities
        selected_city = self.rng.choices(unvisited_cities, weights=probabilities, k=1)[0]
        return selected_city

    def _update_pheromones(self, all_tours):
        """
        Updates the pheromone matrix based on evaporation and ant deposits.
        """
        # Phase 1: Evaporation
        for i in range(self.n_cities):
            for j in range(self.n_cities):
                self.pheromones[i][j] *= (1.0 - self.evaporation_rate)
                
        # Phase 2: Deposit new pheromones from all ants
        for tour, tour_length in all_tours:
            deposit_amount = self.q / tour_length if tour_length > 0 else 0
            
            for i in range(self.n_cities):
                city_a = tour[i]
                # Modulo ensures the tour connects back to the start
                city_b = tour[(i + 1) % self.n_cities]
                
                # Deposit symmetrically for undirected TSP
                self.pheromones[city_a][city_b] += deposit_amount
                self.pheromones[city_b][city_a] += deposit_amount
