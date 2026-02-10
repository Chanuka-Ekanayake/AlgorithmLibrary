"""
Count-Min Sketch (CMS) Frequency Estimator
A probabilistic sub-linear space data structure used to estimate 
the frequency of events in a data stream.
"""

import hashlib
from typing import List

class CountMinSketch:
    """
    Estimates item frequencies using a matrix of counters and 
    independent hash functions.
    """

    def __init__(self, width: int = 1000, depth: int = 5):
        """
        Args:
            width: The number of columns in the counter matrix. 
                   Larger width reduces the probability of hash collisions.
            depth: The number of rows (hash functions). 
                   Larger depth reduces the error probability.
        """
        self.width = width
        self.depth = depth
        # Initialize a 2D matrix (depth x width) with zeros
        self.table = [[0] * width for _ in range(depth)]
        
        # Salt values to simulate independent hash functions
        self.salts = [str(i) for i in range(depth)]

    def _hash(self, item: str, salt: str) -> int:
        """
        Maps an item to a specific column index using a salted hash.
        We use MD5 for speed and distribution, then take the modulo.
        """
        h = hashlib.md5((salt + item).encode('utf-8')).hexdigest()
        return int(h, 16) % self.width

    def add(self, item: str, count: int = 1) -> None:
        """
        Increments the frequency count for an item.
        The item is hashed 'depth' times, and each corresponding 
        counter in the matrix is incremented.
        """
        for i in range(self.depth):
            idx = self._hash(item, self.salts[i])
            self.table[i][idx] += count

    def estimate(self, item: str) -> int:
        """
        Estimates the frequency of an item.
        Returns the minimum value across all hash buckets for this item.
        Logic: Since collisions only ever over-estimate (increase the count),
               the minimum value is the most accurate (least biased) estimate.
        """
        estimates = []
        for i in range(self.depth):
            idx = self._hash(item, self.salts[i])
            estimates.append(self.table[i][idx])
            
        # The 'Min' in Count-Min Sketch
        return min(estimates)

    def get_memory_info(self) -> str:
        """Calculates total counters used."""
        total_cells = self.width * self.depth
        return f"{total_cells} counters (approx. {total_cells * 4 / 1024:.2f} KB)"