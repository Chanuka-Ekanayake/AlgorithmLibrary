"""
Unit tests for Newton's Method algorithms.

This test suite covers normal root finding, optimization, and multivariate 
implementations of Newton's Method. It tests for convergence, accuracy, 
and appropriate error handling.
"""

import unittest
import math
from newtons_method import newtons_method_root, newtons_method_optimization, compute_numerical_derivative
from newtons_method_multivariate import newtons_method_multivariate, gaussian_elimination_solve


class TestNewtonsMethodRoot(unittest.TestCase):
    
    def test_basic_polynomial_root(self):
        # f(x) = x^2 - 4
        # f'(x) = 2x
        # roots at x = 2, -2
        def f(x): return x**2 - 4
        def df(x): return 2*x
        
        # Test finding positive root
        root, iters, converged = newtons_method_root(f, df, x0=1.0)
        self.assertTrue(converged)
        self.assertAlmostEqual(root, 2.0, places=6)
        
        # Test finding negative root
        root, iters, converged = newtons_method_root(f, df, x0=-1.0)
        self.assertTrue(converged)
        self.assertAlmostEqual(root, -2.0, places=6)
        
    def test_numerical_derivative(self):
        # f(x) = x^3 - 2x - 5
        # Root is around 2.09455
        def f(x): return x**3 - 2*x - 5
        
        root, iters, converged = newtons_method_root(f, x0=2.0)
        self.assertTrue(converged)
        self.assertAlmostEqual(root, 2.09455148, places=6)
        
    def test_zero_derivative(self):
        # f(x) = x^2, f'(x) = 2x
        # Guess x=0 gives f'(0) = 0
        def f(x): return x**2
        def df(x): return 2*x
        
        with self.assertRaises(ZeroDivisionError):
            newtons_method_root(f, df, x0=0.0)
            
    def test_non_convergence(self):
        # f(x) = x^3 - 2x + 2
        # Starting at x=0 causes oscillation between 0 and 1
        def f(x): return x**3 - 2*x + 2
        
        root, iters, converged = newtons_method_root(f, x0=0.0, max_iter=20)
        self.assertFalse(converged)


class TestNewtonsMethodOptimization(unittest.TestCase):
    
    def test_basic_quadratic_min(self):
        # f(x) = (x - 3)^2 => f'(x) = 2(x - 3), f''(x) = 2
        # Min at x = 3
        def f(x): return (x - 3)**2
        def f_prime(x): return 2*(x - 3)
        def f_double_prime(x): return 2.0
        
        opt, iters, converged = newtons_method_optimization(
            f, f_prime, f_double_prime, x0=0.0
        )
        self.assertTrue(converged)
        self.assertAlmostEqual(opt, 3.0, places=6)

    def test_numerical_derivatives_optimization(self):
        # f(x) = sin(x)
        # Max at pi/2 (approx 1.5708)
        def f(x): return math.sin(x)
        
        opt, iters, converged = newtons_method_optimization(f, x0=1.0)
        self.assertTrue(converged)
        self.assertAlmostEqual(opt, math.pi / 2, places=6)


class TestNewtonsMethodMultivariate(unittest.TestCase):
    
    def test_gaussian_elimination(self):
        # 2x + y = 5
        # 3x - 2y = 4
        # Sol: x = 2, y = 1
        A = [[2.0, 1.0], [3.0, -2.0]]
        b = [5.0, 4.0]
        
        x = gaussian_elimination_solve(A, b)
        self.assertAlmostEqual(x[0], 2.0, places=6)
        self.assertAlmostEqual(x[1], 1.0, places=6)
        
    def test_multivariate_root_finding(self):
        # System:
        # F1(x, y) = x^2 + y^2 - 4 = 0   (circle)
        # F2(x, y) = x^2 - y - 1 = 0    (parabola)
        def F(v):
            x, y = v[0], v[1]
            return [
                x**2 + y**2 - 4.0,
                x**2 - y - 1.0
            ]
            
        def J(v):
            x, y = v[0], v[1]
            return [
                [2*x, 2*y],
                [2*x, -1.0]
            ]
            
        # Initial guess near intersection
        root, iters, converged = newtons_method_multivariate(F, [1.5, 1.0], J=J)
        self.assertTrue(converged)
        
        # Verify root
        fx = F(root)
        self.assertAlmostEqual(fx[0], 0.0, places=6)
        self.assertAlmostEqual(fx[1], 0.0, places=6)

    def test_multivariate_numerical_jacobian(self):
        # Same system as above, but omitting analytical Jacobian.
        def F(v):
            x, y = v[0], v[1]
            return [
                x**2 + y**2 - 4.0,
                x**2 - y - 1.0
            ]
            
        root, iters, converged = newtons_method_multivariate(F, [1.5, 1.0])
        self.assertTrue(converged)
        
        fx = F(root)
        self.assertAlmostEqual(fx[0], 0.0, places=6)
        self.assertAlmostEqual(fx[1], 0.0, places=6)


if __name__ == '__main__':
    unittest.main()
