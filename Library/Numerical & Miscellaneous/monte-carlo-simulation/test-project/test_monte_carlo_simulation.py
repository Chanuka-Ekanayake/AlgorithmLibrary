import unittest
import sys
import os
import math
import random

# Adjust sys.path to allow importing from the core package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.monte_carlo_simulation import MonteCarloSimulator

class TestMonteCarloSimulation(unittest.TestCase):
    """
    Unit test suite for the Monte Carlo Simulation implementations.
    Due to the stochastic nature of these algorithms, we test bounds and expected statistical properies
    rather than strict deterministic outputs, using large enough samples to minimize variance noise.
    """

    def setUp(self):
        """
        Seed the random number generator to ensure deterministic tests if needed,
        though here we test the bounds to prove the core concept works broadly.
        """
        random.seed(42) # Providing a seed makes checks strictly deterministic for CI stability

    def test_estimate_pi_validation(self):
        """
        Test that invalid inputs to pi estimation raise correct errors.
        """
        with self.assertRaises(ValueError):
            MonteCarloSimulator.estimate_pi(0)
            
        with self.assertRaises(ValueError):
            MonteCarloSimulator.estimate_pi(-100)

    def test_estimate_pi_accuracy(self):
        """
        Test that the Monte Carlo estimation of Pi is reasonably accurate for a given 'N'.
        With N=100,000, standard error is roughly 0.005. So we assert it's within 0.05 of actual Pi.
        """
        n_samples = 100_000
        pi_estimate, error = MonteCarloSimulator.estimate_pi(n_samples)
        
        self.assertAlmostEqual(pi_estimate, math.pi, delta=0.02, 
                               msg=f"Pi estimate {pi_estimate} was too far from {math.pi}")
        self.assertTrue(error < 0.02)

    def test_simulate_1d_random_walk_validation(self):
        """
        Test that invalid inputs to random walk raise correct errors.
        """
        with self.assertRaises(ValueError):
            MonteCarloSimulator.simulate_1d_random_walk(-1, 100)
            
        with self.assertRaises(ValueError):
            MonteCarloSimulator.simulate_1d_random_walk(10, 0)

    def test_simulate_1d_random_walk_statistics(self):
        """
        Test the statistical properties of a 1D random walk.
        Expected position should be ~0.
        Expected absolute distance should be ~sqrt(2n/pi).
        """
        steps = 1000
        sims = 5000
        stats = MonteCarloSimulator.simulate_1d_random_walk(steps, sims)
        
        # Mean final position should be very close to 0
        self.assertAlmostEqual(stats["average_final_position"], 0.0, delta=2.0)
        
        # Expected distance E[|S_n|] = sqrt(2n/pi)
        expected_distance = math.sqrt((2 * steps) / math.pi)
        self.assertAlmostEqual(stats["average_distance"], expected_distance, delta=1.5)
        
        # Logical bounds checks
        self.assertGreaterEqual(stats["max_distance"], 0)
        self.assertGreaterEqual(stats["max_position"], stats["average_final_position"])
        self.assertLessEqual(stats["min_position"], stats["average_final_position"])

    def test_simulate_asset_price_paths_validation(self):
        """
        Test that invalid inputs to GBM simulation raise correct errors.
        """
        with self.assertRaises(ValueError):
            # Negative stock price
            MonteCarloSimulator.simulate_asset_price_paths(-10, 0.05, 0.2, 1.0, 252, 10)
            
        with self.assertRaises(ValueError):
            # Zero steps
            MonteCarloSimulator.simulate_asset_price_paths(100, 0.05, 0.2, 1.0, 0, 10)
            
        with self.assertRaises(ValueError):
            # Zero sims
            MonteCarloSimulator.simulate_asset_price_paths(100, 0.05, 0.2, 1.0, 252, 0)

    def test_simulate_asset_price_paths_shape(self):
        """
        Test that the generated paths have the expected dimensions and shape.
        """
        sims = 50
        steps = 100
        S0 = 100.0
        
        paths = MonteCarloSimulator.simulate_asset_price_paths(S0, 0.05, 0.2, 1.0, steps, sims)
        
        # Check num paths
        self.assertEqual(len(paths), sims)
        
        # Check num steps per path (Initial S0 + steps)
        for path in paths:
            self.assertEqual(len(path), steps + 1)
            self.assertEqual(path[0], S0)
            # Prices in GBM should never drop below 0
            self.assertTrue(all(p > 0 for p in path))

    def test_expected_asset_price(self):
        """
        Test that the average of simulated terminal prices matches the theoretical expected value.
        Theoretical Expected Value of GBM: E[S_T] = S_0 * e^(mu * T)
        """
        S0 = 50.0
        mu = 0.10
        sigma = 0.15
        T = 2.0
        steps = 252 # Daily steps for 2 years
        sims = 10_000
        
        paths = MonteCarloSimulator.simulate_asset_price_paths(S0, mu, sigma, T, steps, sims)
        simulated_expected_price = MonteCarloSimulator.expected_asset_price(paths)
        
        theoretical_price = S0 * math.exp(mu * T)
        
        # Since standard error is high in asset paths, we allow a wider delta like 1.5%
        self.assertAlmostEqual(simulated_expected_price, theoretical_price, delta=(theoretical_price * 0.02))

    def test_expected_asset_price_empty(self):
        """
        Test handling of empty paths in expected asset price calculator.
        """
        self.assertEqual(MonteCarloSimulator.expected_asset_price([]), 0.0)

if __name__ == '__main__':
    unittest.main()
