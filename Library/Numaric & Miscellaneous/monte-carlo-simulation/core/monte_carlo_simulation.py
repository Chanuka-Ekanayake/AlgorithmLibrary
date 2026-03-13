import random
import math
from typing import List, Tuple, Dict, Any

class MonteCarloSimulator:
    """
    A collection of classic Monte Carlo Simulations showcasing the use of randomness
    to solve deterministic mathematical problems and simulate complex probabilistic systems.
    """

    @staticmethod
    def estimate_pi(num_samples: int) -> Tuple[float, float]:
        """
        Estimates the value of Pi (π) using the Monte Carlo method.
        
        Imagine a square of side length 2 centered at the origin (x=0, y=0).
        The area of the square is 2 * 2 = 4.
        Inside this square, imagine a circle with radius 1.
        The area of the circle is π * r^2 = π * 1^2 = π.
        
        The ratio of the area of the circle to the area of the square is π / 4.
        If we randomly throw darts at this square, the probability of a dart landing
        inside the circle is exactly π / 4.
        
        :param num_samples: The number of random points (darts) to generate.
        :return: A tuple containing (estimated_pi_value, absolute_error).
        """
        if num_samples <= 0:
            raise ValueError("Number of samples must be a positive integer.")

        points_inside_circle = 0
        
        for _ in range(num_samples):
            # Generate random x and y between -1.0 and 1.0
            x = random.uniform(-1.0, 1.0)
            y = random.uniform(-1.0, 1.0)
            
            # Check if the point (x,y) lies inside the circle of radius 1
            # Equation of a circle: x^2 + y^2 <= r^2
            if x**2 + y**2 <= 1.0:
                points_inside_circle += 1
                
        # (points in circle / total points) ≈ (π / 4)
        # π ≈ 4 * (points in circle / total points)
        pi_estimate = 4 * (points_inside_circle / num_samples)
        absolute_error = abs(math.pi - pi_estimate)
        
        return pi_estimate, absolute_error

    @staticmethod
    def simulate_1d_random_walk(num_steps: int, num_simulations: int) -> Dict[str, Any]:
        """
        Simulates multiple 1D random walks.
        
        A particle starts at position 0. At each step, it has a 50% chance to move right (+1)
        and a 50% chance to move left (-1).
        
        This simulation calculates the final positions of multiple walks and computes
        the expected distance from the origin.
        
        :param num_steps: Number of steps each particle takes.
        :param num_simulations: Number of independent random walks to simulate.
        :return: A dictionary containing statistics about the final positions.
        """
        if num_steps < 0 or num_simulations <= 0:
            raise ValueError("Steps must be non-negative and simulations must be positive.")

        final_positions = []
        distances_from_origin = []

        for _ in range(num_simulations):
            position = 0
            for _ in range(num_steps):
                # Random choice: -1 or 1
                step = random.choice([-1, 1])
                position += step
                
            final_positions.append(position)
            distances_from_origin.append(abs(position))

        average_final_position = sum(final_positions) / num_simulations
        average_distance = sum(distances_from_origin) / num_simulations
        
        return {
            "num_simulations": num_simulations,
            "num_steps": num_steps,
            "average_final_position": average_final_position, # Should be close to 0
            "average_distance": average_distance,             # Should scale with sqrt(steps)
            "max_distance": max(distances_from_origin),
            "min_position": min(final_positions),
            "max_position": max(final_positions)
        }

    @staticmethod
    def simulate_asset_price_paths(
        S0: float, 
        mu: float, 
        sigma: float, 
        time_horizon_years: float, 
        time_steps: int, 
        num_simulations: int
    ) -> List[List[float]]:
        """
        Simulates future paths of an asset price (like a stock) using Geometric Brownian Motion (GBM).
        
        This is a common Monte Carlo application in quantitative finance to price derivatives.
        
        :param S0: Initial stock price (e.g., 100.0).
        :param mu: Expected annual annualized return/drift (e.g., 0.05 for 5%).
        :param sigma: Annualized volatility/standard deviation (e.g., 0.20 for 20%).
        :param time_horizon_years: Time horizon in years (e.g., 1.0 for 1 year).
        :param time_steps: Number of discrete time steps to model within the horizon (e.g., 252 trading days).
        :param num_simulations: Number of unique paths to simulate.
        :return: A list of simulated price paths. Each path is a list of prices over time.
        """
        if time_steps <= 0 or num_simulations <= 0:
            raise ValueError("Time steps and number of simulations must be positive integers.")
        if time_horizon_years <= 0:
            raise ValueError("Time horizon must be positive.")
        if S0 < 0:
            raise ValueError("Initial stock price must be non-negative.")

        dt = time_horizon_years / time_steps
        paths = []

        for _ in range(num_simulations):
            # Start a new path at the initial price
            path = [S0]
            current_price = S0
            
            for _ in range(time_steps):
                # Generate a random shock from a standard normal distribution N(0,1)
                Z = random.gauss(0, 1)
                
                # Geometric Brownian Motion formula
                # dS = S * (mu * dt + sigma * dW)
                # S(t+dt) = S(t) * exp((mu - 0.5 * sigma^2) * dt + sigma * sqrt(dt) * Z)
                drift_term = (mu - 0.5 * sigma**2) * dt
                shock_term = sigma * math.sqrt(dt) * Z
                
                next_price = current_price * math.exp(drift_term + shock_term)
                path.append(next_price)
                current_price = next_price
                
            paths.append(path)
            
        return paths

    @staticmethod
    def expected_asset_price(paths: List[List[float]]) -> float:
        """
        Calculates the expected (average) final price of an asset across all simulated paths.
        
        :param paths: List of simulated price paths generated by `simulate_asset_price_paths`.
        :return: The average final price.
        """
        if not paths:
            return 0.0
            
        final_prices = [path[-1] for path in paths]
        return sum(final_prices) / len(final_prices)

if __name__ == "__main__":
    print("=== Monte Carlo Simulations ===\n")

    # 1. Estimating Pi
    samples = 1_000_000
    print(f"1. Estimating Pi with {samples:,} samples...")
    pi_est, err = MonteCarloSimulator.estimate_pi(samples)
    print(f"   Estimated Pi : {pi_est}")
    print(f"   Actual Pi    : {math.pi}")
    print(f"   Error        : {err:.6f}\n")

    # 2. 1D Random Walk
    steps = 1000
    sims = 5000
    print(f"2. Simulating 1D Random Walk ({steps} steps, {sims} simulations)...")
    rw_stats = MonteCarloSimulator.simulate_1d_random_walk(steps, sims)
    print(f"   Average Final Position : {rw_stats['average_final_position']:.3f} (Expected ~0)")
    # For a simple random walk, expected distance is approx sqrt(2*N/pi) ≈ 0.8 * sqrt(N)
    # Actually, expected absolute distance E[|S_n|] ≈ sqrt(2n/pi)
    expected_dist = math.sqrt(2 * steps / math.pi)
    print(f"   Average Distance       : {rw_stats['average_distance']:.3f} (Theoretical ~{expected_dist:.3f})\n")

    # 3. Asset Price Modeling (Geometric Brownian Motion)
    S0 = 100.0        # $100 initial stock price
    mu = 0.08         # 8% expected annual return
    sigma = 0.20      # 20% annual volatility
    horizon = 1.0     # 1 year
    trading_days = 252 # Daily steps
    paths_count = 10000

    print(f"3. Simulating Asset Prices (GBM)")
    print(f"   S0=${S0}, Return={mu*100}%, Volatility={sigma*100}%, Horizon={horizon}yr, {paths_count} sims...")
    
    paths = MonteCarloSimulator.simulate_asset_price_paths(S0, mu, sigma, horizon, trading_days, paths_count)
    exp_price = MonteCarloSimulator.expected_asset_price(paths)
    
    # The theoretical expected value of GBM is S0 * e^(mu * t)
    theoretical_price = S0 * math.exp(mu * horizon)
    
    print(f"   Simulated Expected Price : ${exp_price:.2f}")
    print(f"   Theoretical Expected Price: ${theoretical_price:.2f}")
    print(f"   Max Price observed       : ${max(p[-1] for p in paths):.2f}")
    print(f"   Min Price observed       : ${min(p[-1] for p in paths):.2f}")
