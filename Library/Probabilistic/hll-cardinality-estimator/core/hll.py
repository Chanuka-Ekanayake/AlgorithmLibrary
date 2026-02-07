"""
HyperLogLog (HLL) Cardinality Estimator
Uses probabilistic counting to estimate the number of unique elements
in a stream with high accuracy and minimal memory footprint.
"""

import hashlib
import math
from typing import Any

class HyperLogLog:
    """
    Implements the HyperLogLog algorithm for near-constant space 
    cardinality estimation.
    """

    def __init__(self, precision: int = 10):
        """
        Args:
            precision: Determines the number of buckets (m = 2^precision).
                       Higher precision reduces the error rate but uses more memory.
                       Standard error is approx 1.04 / sqrt(m).
        """
        self.p = precision
        self.m = 1 << precision  # Number of registers (buckets)
        self.registers = [0] * self.m
        
        # Alpha constant for bias correction based on m
        if self.m == 16:
            self.alpha = 0.673
        elif self.m == 32:
            self.alpha = 0.697
        elif self.m == 64:
            self.alpha = 0.709
        else:
            self.alpha = 0.7213 / (1 + 1.079 / self.m)

    def _get_hash(self, value: Any) -> int:
        """Generates a 64-bit hash of the input value."""
        # We use SHA-256 and take the first 64 bits (16 hex chars)
        h_hex = hashlib.sha256(str(value).encode('utf-8')).hexdigest()
        return int(h_hex[:16], 16)

    def add(self, item: Any) -> None:
        """
        Adds an item to the estimator.
        1. Hashes the item.
        2. Uses the first 'p' bits to pick a register.
        3. Counts leading zeros in the remaining bits to estimate cardinality.
        """
        x = self._get_hash(item)
        
        # Extract the register index (first p bits)
        idx = x & (self.m - 1)
        
        # Extract the value for zero-counting (remaining bits)
        w = x >> self.p
        
        # Count leading zeros (plus 1 for the first set bit)
        # We simulate this by checking the position of the first '1' bit
        rho = self._count_leading_zeros(w)
        
        # Keep the maximum zero count seen so far for this register
        self.registers[idx] = max(self.registers[idx], rho)

    def _count_leading_zeros(self, w: int) -> int:
        """Returns the position of the first 1-bit from the right."""
        if w == 0:
            return 64 - self.p # Max possible zeros for a 64-bit hash
        
        # Standard bit-manipulation to find the first '1'
        return (w & -w).bit_length()

    def count(self) -> int:
        """
        Estimates the total number of unique elements using the 
        harmonic mean of the registers.
        """
        # Calculate the raw estimate using the harmonic mean
        z = sum(2.0 ** -r for r in self.registers)
        estimate = self.alpha * (self.m ** 2) / z
        
        # Small range correction (Linear Counting)
        if estimate <= 2.5 * self.m:
            zeros = self.registers.count(0)
            if zeros != 0:
                estimate = self.m * math.log(self.m / zeros)
        
        # Note: Large range correction is omitted for simplicity as 
        # it only applies to estimates approaching 2^64.
        
        return int(estimate)

    def get_memory_usage(self) -> str:
        """Calculates approximate memory footprint of the registers."""
        # Each register is typically 1 byte (can store up to 64)
        return f"{self.m} bytes (Registers only)"