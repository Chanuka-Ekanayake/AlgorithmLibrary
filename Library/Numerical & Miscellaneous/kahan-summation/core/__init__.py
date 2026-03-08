"""
Kahan Summation Algorithm Core Module.

This module exposes the main functional API and the class-based Accumulator 
to perform compensated summation. It hides the underlying complexities 
and provides a clean interface for consumers.
"""

from .accumulator import KahanAccumulator, kahan_sum, naive_sum

__all__ = [
    "KahanAccumulator",
    "kahan_sum",
    "naive_sum"
]
