"""
Fisher-Yates (Knuth) Shuffler
Provides a mathematically unbiased, O(n) in-place randomization algorithm.
Ensures that every permutation of a list is equally probable.
"""

import random
from typing import List, Any, Dict

class FisherYatesShuffler:
    """
    Engine for unbiased list randomization.
    """

    @staticmethod
    def shuffle(items: List[Any]) -> List[Any]:
        """
        Shuffles a list in-place using the Fisher-Yates logic.
        
        Args:
            items: The list to be randomized.
            
        Returns:
            The same list object, randomized.
        """
        n = len(items)
        if n <= 1:
            return items

        # Iterate from the last element down to the second element
        for i in range(n - 1, 0, -1):
            # Pick a random index 'j' such that 0 <= j <= i
            # This is the "Modern" Fisher-Yates approach
            j = random.randint(0, i)
            
            # Swap items[i] and items[j]
            items[i], items[j] = items[j], items[i]
            
        return items

    @staticmethod
    def get_distribution_stats(items: List[Any], iterations: int = 10000) -> Dict[str, int]:
        """
        Analytical tool to verify the fairness of the shuffle.
        Useful for unit testing and regulatory compliance.
        
        Returns a dictionary showing how many times each sequence appeared.
        """
        stats: Dict[str, int] = {}
        
        for _ in range(iterations):
            # Create a copy to avoid mutating the original reference during testing
            test_copy = list(items)
            shuffled = FisherYatesShuffler.shuffle(test_copy)
            result_str = " -> ".join(map(str, shuffled))
            
            stats[result_str] = stats.get(result_str, 0) + 1
            
        return stats