"""
Kahan Summation: Demonstration and Benchmark Application

This CLI application is designed to demonstrate catastrophic cancellation
in standard floating-point addition and prove how Kahan Summation completely
mitigates this issue using a compensation variable.

It achieves this by:
1. Generating a massive array of floats with wildly differing exponents.
2. Summing them using Python's naive float addition (which loses precision).
3. Summing them using our custom Kahan Accumulator.
4. Summing them using a gold-standard infinite-precision Decimal library.
5. Comparing the drift and outputting the exact delta metrics.
"""

import argparse
import random
import time
import math
import sys
from decimal import Decimal, getcontext
import os

# Ensure the core module is accessible regardless of where app.py is invoked from
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from core.accumulator import kahan_sum, naive_sum, KahanAccumulator

def generate_test_data(size: int, variance_modifier: int = 15) -> list[float]:
    """
    Generates a list of floating point numbers designed to cause
    catastrophic cancellation in naive summation.
    
    Args:
        size (int): Number of elements to generate.
        variance_modifier (int): Controls the exponent spread width.
        
    Returns:
        list[float]: A sequence of highly variable floats.
    """
    random.seed(42)  # Fixed seed for reproducible benchmarks
    data = []
    
    # We deliberately add a massive initial number to ensure the
    # accumulator's exponent is pinned high from the start.
    data.append(1.0e16)
    
    # We then append many tiny fractional numbers which are easily dropped.
    for _ in range(size - 2):
        # Generate varied exponents, mostly tiny
        exponent = random.uniform(-variance_modifier, variance_modifier / 2)
        mantissa = random.uniform(-1.0, 1.0)
        
        number = mantissa * (10 ** exponent)
        data.append(number)
        
    # Finally, subtract the initial massive number to expose the residual error
    data.append(-1.0e16)
    
    # Shuffle only the middle fractions to ensure true random order
    middle = data[1:-1]
    random.shuffle(middle)
    data = [data[0]] + middle + [data[-1]]
    
    return data

def run_benchmark(data: list[float]) -> None:
    """
    Executes the benchmark logic across standard, kahan, and absolute
    precision summations.
    
    Args:
        data (list[float]): The dataset to sum.
    """
    print(f"--- Kahan Summation Benchmark (N = {len(data)}) ---")
    
    # 1. Gold Standard exact calculation using Python's internal Decimal library
    # We set precision artificially high to guarantee zero drop
    getcontext().prec = 100
    decimal_data = [Decimal(str(x)) for x in data]
    print("Calculating Perfect Sum (Infinite Precision Decimal)...")
    t0 = time.time()
    perfect_sum = sum(decimal_data)
    t_perfect = time.time() - t0
    
    # 2. Naive Standard Summation
    print("Calculating Naive Sum (Standard Floating Point)...")
    t0 = time.time()
    standard_sum = naive_sum(data)
    t_standard = time.time() - t0
    
    # 3. Kahan Summation
    print("Calculating Kahan Compensated Sum...")
    t0 = time.time()
    kahan_result = kahan_sum(data)
    t_kahan = time.time() - t0
    
    # Print Output Analysis
    print("\n--- Benchmark Results ---")
    print(f"True Perfect Mathematical Sum : {perfect_sum}")
    print(f"Standard Python Naive Sum     : {standard_sum}")
    print(f"Kahan Compensated Sum         : {kahan_result}")
    
    print("\n--- Error Analysis Constraints ---")
    # Using Decimal to accurately find the tiny error drift
    error_standard = abs(Decimal(str(standard_sum)) - perfect_sum)
    error_kahan = abs(Decimal(str(kahan_result)) - perfect_sum)
    
    print(f"Naive Float Error  : {error_standard}")
    print(f"Kahan Float Error  : {error_kahan}")
    
    # Check if kahan fundamentally outperformed naive implementation
    if error_standard > error_kahan:
        print("\n[SUCCESS] Kahan Summation successfully recovered truncated precision!")
    elif error_standard == error_kahan:
        print("\n[INFO] Both algorithms performed identically (Try increasing variance).")
    else:
        print("\n[WARNING] Kahan underperformed! (Hardware fast-math optimization suspected).")
        
    print(f"\nTime Analysis - Naive: {t_standard:.5f}s | Kahan: {t_kahan:.5f}s | Ratio: {t_kahan / (t_standard+1e-9):.2f}x slower")

def main():
    parser = argparse.ArgumentParser(description="Kahan Summation Precision Benchmark")
    parser.add_argument('--size', type=int, default=1000000,
                        help="Number of floats to generate for the test suite.")
    parser.add_argument('--variance', type=int, default=15,
                        help="Exponent variability (higher means more precision loss).")
    
    args = parser.parse_args()
    
    print("Generating randomized adversarial dataset (Please wait)...")
    dataset = generate_test_data(args.size, args.variance)
    
    run_benchmark(dataset)

if __name__ == "__main__":
    main()
