"""
Dynamic Programming Allocation Engine (Coin Change)
Calculates the mathematically optimal combination of resource bundles 
to fulfill an exact target amount without over-allocating.
"""

from typing import List

class ResourceOptimizer:
    """
    Allocates exact API credits or compute units using Dynamic Programming.
    """

    @staticmethod
    def get_optimal_allocation(bundles: List[int], target: int) -> List[int]:
        """
        Determines the exact combination of bundles needed to hit the target.
        
        Args:
            bundles: Available bundle denominations (e.g., [100, 500, 1000]).
            target: The exact requested amount of credits.
            
        Returns:
            A list of the specific bundles used to fulfill the target.
            Returns an empty list if the target is 0.
            Raises ValueError if the target cannot be fulfilled exactly.
        """
        if target < 0:
            raise ValueError("Target allocation amount cannot be negative.")
        if target == 0:
            return []

        # Validate bundle denominations to ensure safe DP indexing
        for bundle in bundles:
            if not isinstance(bundle, int) or bundle <= 0:
                raise ValueError(f"Invalid bundle denomination {bundle!r}. "
                                 "All bundle values must be positive integers.")
        # 1. Initialize the DP Array
        # dp[i] will store the minimum number of bundles needed for amount 'i'.
        # We use (target + 1) as our "infinity" placeholder.
        infinity = target + 1
        dp = [infinity] * (target + 1)
        dp[0] = 0
        
        # 2. Initialize the State Tracker
        # tracker[i] stores the value of the last bundle added to reach amount 'i'.
        # This is essential for reconstructing the final list of bundles.
        tracker = [-1] * (target + 1)

        # 3. Build the DP Table (Bottom-Up)
        for current_amount in range(1, target + 1):
            for bundle in bundles:
                # If this bundle can fit into the current amount we are trying to build...
                if current_amount - bundle >= 0:
                    
                    # Calculate if using this bundle results in fewer total bundles
                    # than our current known best way to reach 'current_amount'.
                    potential_new_min = 1 + dp[current_amount - bundle]
                    
                    if potential_new_min < dp[current_amount]:
                        dp[current_amount] = potential_new_min
                        # Remember exactly which bundle gave us this new minimum
                        tracker[current_amount] = bundle

        # 4. Check for Impossibility
        if dp[target] == infinity:
            raise ValueError(f"Target amount {target} cannot be fulfilled with available bundles: {bundles}")

        # 5. Backtrack to Reconstruct the Receipt
        allocation = []
        remaining_target = target
        
        # Walk backward through the tracker array until we hit 0
        while remaining_target > 0:
            used_bundle = tracker[remaining_target]
            # Defensive check: ensure the tracker contains a valid, positive bundle
            if used_bundle <= 0:
                raise ValueError(
                    f"Inconsistent allocation state: no valid bundle recorded for remaining target "
                    f"{remaining_target} with bundles {bundles}."
                )
            allocation.append(used_bundle)
            remaining_target -= used_bundle

        # Return the final list of allocated bundles (sorted for readability)
        return sorted(allocation, reverse=True)