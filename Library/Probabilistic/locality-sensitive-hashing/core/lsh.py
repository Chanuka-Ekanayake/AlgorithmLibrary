"""
Locality-Sensitive Hashing (LSH) - Similarity Search Module
Uses Random Projections to hash high-dimensional vectors into 
buckets, enabling sub-linear approximate nearest neighbor search.
"""

import numpy as np
from typing import List, Dict, Any

class RandomProjectionLSH:
    """
    LSH implementation for Cosine Similarity using the 
    Random Projection (SimHash) method.
    """

    def __init__(self, dimensions: int, num_projections: int = 12):
        """
        Args:
            dimensions: Size of the input vectors (e.g., embedding size).
            num_projections: Number of random planes. Higher values 
                             increase precision but reduce recall.
        """
        self.dimensions = dimensions
        self.num_projections = num_projections
        
        # Create random hyperplanes (normally distributed)
        # These act as the 'axes' we project our vectors onto
        self.planes = np.random.randn(num_projections, dimensions)
        
        # Hash table: {binary_string_signature: [item_ids]}
        self.buckets: Dict[str, List[Any]] = {}

    def _generate_signature(self, vector: np.ndarray) -> str:
        """
        Projects a vector onto random planes.
        - Positive projection -> '1'
        - Negative/Zero projection -> '0'
        Result is a binary string 'signature'.
        """
        # Dot product of the vector with all planes at once
        projections = np.dot(self.planes, vector)
        
        # Convert to bitstring: 1 if >= 0, else 0
        bits = (projections >= 0).astype(int)
        return "".join(map(str, bits))

    def add_item(self, item_id: Any, vector: List[float]) -> None:
        """
        Hashes a vector and stores the item_id in the corresponding bucket.
        """
        vec_np = np.array(vector)
        signature = self._generate_signature(vec_np)
        
        if signature not in self.buckets:
            self.buckets[signature] = []
        
        self.buckets[signature].append(item_id)

    def query(self, vector: List[float]) -> List[Any]:
        """
        Finds candidate similar items by looking in the same bucket.
        Returns the IDs of items in the collision bucket.
        """
        vec_np = np.array(vector)
        signature = self._generate_signature(vec_np)
        
        # Return a shallow copy of candidates from the same bucket (if any)
        return list(self.buckets.get(signature, []))

    def get_stats(self) -> Dict[str, int]:
        """Returns the distribution of items across buckets."""
        return {
            "total_buckets": len(self.buckets),
            "max_items_in_bucket": max((len(v) for v in self.buckets.values()), default=0),
            "total_items": sum(len(v) for v in self.buckets.values())
        }