from typing import List, Tuple

class KnapsackOptimizer:
    """
    Implements the 0/1 Knapsack algorithm to solve combinatorial 
    optimization problems for resource allocation.
    """

    @staticmethod
    def solve(values: List[int], weights: List[int], capacity: int) -> Tuple[int, List[int]]:
        """
        Solves the 0/1 Knapsack problem using a bottom-up DP table.
        
        Args:
            values: List of item values.
            weights: List of item weights (e.g., cost, RAM, storage).
            capacity: The maximum capacity of the knapsack (e.g., budget, total RAM).
            
        Returns:
            A tuple containing (max_value, indices_of_selected_items).
        """
        n = len(values)
        # dp[i][w] will store the maximum value that can be attained 
        # with weight less than or equal to w using items from the first i items.
        dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

        # Build the table in bottom-up fashion
        for i in range(1, n + 1):
            for w in range(1, capacity + 1):
                if weights[i-1] <= w:
                    # Choice: Include the item or exclude it
                    dp[i][w] = max(
                        values[i-1] + dp[i-1][w - weights[i-1]], 
                        dp[i-1][w]
                    )
                else:
                    # Item is too heavy, must exclude it
                    dp[i][w] = dp[i-1][w]

        # Reconstruct the set of items included in the optimal solution
        max_value = dp[n][capacity]
        selected_indices = []
        w = capacity
        for i in range(n, 0, -1):
            if dp[i][w] != dp[i-1][w]:
                selected_indices.append(i - 1)
                w -= weights[i-1]

        return max_value, selected_indices[::-1]