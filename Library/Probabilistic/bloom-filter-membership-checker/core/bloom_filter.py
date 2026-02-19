import math
import hashlib
from typing import Any

class BloomFilter:
    """
    A space-efficient probabilistic data structure.
    Used to check if an element is a member of a set.
    """

    def __init__(self, expected_items: int, false_positive_rate: float):
        """
        Calculates optimal size and number of hash functions.
        """
        # Size of bit array (m)
        self.size = self._get_size(expected_items, false_positive_rate)
        
        # Number of hash functions (k)
        self.hash_count = self._get_hash_count(self.size, expected_items)
        
        # Initialize bit array with 0s
        self.bit_array = [0] * self.size

    def add(self, item: str):
        """Sets bits at k indices calculated via hashing."""
        for i in range(self.hash_count):
            index = self._hash(item, i)
            self.bit_array[index] = 1

    def exists(self, item: str) -> bool:
        """
        Checks if item might be in the set.
        Returns False if definitely not present.
        Returns True if possibly present (False Positive possible).
        """
        for i in range(self.hash_count):
            index = self._hash(item, i)
            if self.bit_array[index] == 0:
                return False
        return True

    def _hash(self, item: str, seed: int) -> int:
        """Generates a hash for an item given a specific seed."""
        hash_val = hashlib.sha256((str(item) + str(seed)).encode()).hexdigest()
        return int(hash_val, 16) % self.size

    @staticmethod
    def _get_size(n, p):
        """m = -(n * ln(p)) / (ln(2)^2)"""
        m = -(n * math.log(p)) / (math.log(2) ** 2)
        return int(m)

    @staticmethod
    def _get_hash_count(m, n):
        """k = (m/n) * ln(2)"""
        k = (m / n) * math.log(2)
        return int(k)