"""
Fast Fourier Transform (FFT) - Cooley-Tukey Algorithm
Transforms a signal from the time domain to the frequency domain.
"""

import math
import cmath
from typing import List

def fft(x: List[complex]) -> List[complex]:
    """
    Recursive implementation of the 1D Cooley-Tukey FFT.
    N must be a power of 2.
    """
    n = len(x)
    
    # Base Case: The Fourier Transform of a single point is itself.
    if n <= 1:
        return x
    
    # Structural Constraint: Ensure the signal length is a power of 2.
    if n % 2 != 0:
        raise ValueError("N must be a power of 2.")

    # Divide: Separate the signal into even and odd indexed samples.
    # This is the 'Decimation-in-Time' approach.
    even = fft(x[0::2])
    odd = fft(x[1::2])
    
    # Conquer: Combine the results using the 'Butterfly' operation.
    # We pre-calculate complex 'Twiddle Factors' to avoid redundant math.
    combined = [0j] * n 
    
    for k in range(n // 2):
        # Angle calculation: -2 * pi * k / N
        angle = -2 * math.pi * k / n
        twiddle = cmath.exp(complex(0, angle)) * odd[k]
        
        # Butterfly step: Sum and difference of the even and odd parts
        combined[k] = even[k] + twiddle
        combined[k + n // 2] = even[k] - twiddle
        
    return combined

def get_magnitude(complex_signal: List[complex]) -> List[float]:
    """Extracts magnitude: sqrt(real^2 + imag^2)."""
    return [abs(c) for c in complex_signal]