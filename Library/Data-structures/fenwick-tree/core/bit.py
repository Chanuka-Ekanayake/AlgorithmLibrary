"""
Fenwick Tree (Binary Indexed Tree)
A highly memory-efficient data structure for maintaining cumulative frequencies 
and calculating prefix sums in O(log N) time using bitwise operations.
"""

from typing import List

class FenwickTree:
    """
    Provides O(log N) point updates and range queries for continuous data streams.
    """
    
    def __init__(self, size: int):
        """
        Initializes an empty Fenwick Tree.
        
        Args:
            size: The maximum number of elements the tree will hold.
        """
        if size <= 0:
            raise ValueError("Tree size must be strictly positive.")
            
        self.size = size
        # BIT strictly uses 1-based indexing. Index 0 is ignored because 
        # bitwise operations on 0 cause infinite loops.
        self.tree = [0.0] * (size + 1)

    @classmethod
    def build_from_array(cls, values: List[float]) -> "FenwickTree":
        """
        Bulk-builds a Fenwick Tree in O(N) time instead of O(N log N).
        Ideal for initializing historical data before accepting live updates.
        """
        n = len(values)
        bit = cls(n)
        
        # 1. Copy the original values into the tree array (1-indexed)
        for i in range(n):
            bit.tree[i + 1] = values[i]
            
        # 2. Propagate the values to their mathematical parents
        for i in range(1, n + 1):
            parent_index = i + (i & (-i))
            if parent_index <= n:
                bit.tree[parent_index] += bit.tree[i]
                
        return bit

    def add(self, index: int, delta: float) -> None:
        """
        Updates a value at the given index (1-based) by adding 'delta', 
        and propagates the change up the tree.
        
        Args:
            index: The 1-based index to update.
            delta: The value to add (can be negative for subtractions).
        """
        if index <= 0 or index > self.size:
            raise IndexError(f"Index {index} out of bounds for tree of size {self.size}.")
            
        while index <= self.size:
            self.tree[index] += delta
            # Move to the parent node by ADDING the Least Significant Bit (LSB)
            index += index & (-index)

    def query_prefix(self, index: int) -> float:
        """
        Calculates the cumulative sum from index 1 to the given index.
        
        Args:
            index: The 1-based upper bound index.
            
        Returns:
            The cumulative sum.
        """
        if index < 0 or index > self.size:
            raise IndexError(f"Index {index} out of bounds for tree of size {self.size}.")
            
        total = 0.0
        while index > 0:
            total += self.tree[index]
            # Move to the preceding node by SUBTRACTING the Least Significant Bit (LSB)
            index -= index & (-index)
            
        return total

    def query_range(self, left: int, right: int) -> float:
        """
        Calculates the sum of elements precisely between 'left' and 'right' (inclusive).
        
        Args:
            left: The 1-based lower bound index.
            right: The 1-based upper bound index.
            
        Returns:
            The sum of the specified range.
        """
        if left > right:
            raise ValueError("Left index cannot be greater than right index.")
        if left <= 0 or right > self.size:
            raise IndexError("Range out of bounds.")
            
        # The sum from L to R is simply the sum up to R minus the sum up to (L-1)
        return self.query_prefix(right) - self.query_prefix(left - 1)