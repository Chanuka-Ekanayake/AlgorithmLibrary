"""
Longest Increasing Subsequence (LIS)
Implements sequence analysis using both standard Dynamic Programming 
and highly optimized Binary Search methodologies.
"""

import bisect
from typing import List, Tuple

class LongestIncreasingSubsequence:
    """
    Analyzes numerical sequences to find the longest strictly increasing subsequence.
    """

    @staticmethod
    def classic_dp(arr: List[int]) -> Tuple[int, List[int]]:
        """
        Computes the LIS using classic Dynamic Programming.
        Time Complexity: O(N^2)
        Space Complexity: O(N)
        
        Returns:
            Tuple containing (length_of_lis, actual_sequence)
        """
        if not arr:
            return 0, []

        n = len(arr)
        # dp[i] stores the length of the LIS ending at index i
        dp = [1] * n
        # parent[i] stores the index of the previous element in the LIS
        parent = [-1] * n

        for i in range(1, n):
            for j in range(i):
                if arr[i] > arr[j] and dp[i] < dp[j] + 1:
                    dp[i] = dp[j] + 1
                    parent[i] = j

        # Find the index of the maximum value in dp
        max_len = 0
        best_end_index = -1
        for i in range(n):
            if dp[i] > max_len:
                max_len = dp[i]
                best_end_index = i

        # Reconstruct the sequence
        sequence = []
        curr = best_end_index
        while curr != -1:
            sequence.append(arr[curr])
            curr = parent[curr]

        return max_len, sequence[::-1]

    @staticmethod
    def optimal_binary_search(arr: List[int]) -> Tuple[int, List[int]]:
        """
        Computes the LIS using Binary Search (Patience Sorting).
        Time Complexity: O(N log N)
        Space Complexity: O(N)
        
        Returns:
            Tuple containing (length_of_lis, actual_sequence)
        """
        if not arr:
            return 0, []

        # tails_indices[i] stores the index in 'arr' of the smallest tail 
        # of an increasing subsequence of length i+1.
        tails_indices = []
        # parent[i] stores the index of the predecessor of arr[i] in the LIS
        parent = [-1] * len(arr)

        for i, x in enumerate(arr):
            # We use binary search to find the insertion point for x
            # based on the values pointed to by tails_indices.
            # We can't use bisect directly on a list of indices, so we do a custom binary search:
            left, right = 0, len(tails_indices)
            while left < right:
                mid = (left + right) // 2
                if arr[tails_indices[mid]] < x:
                    left = mid + 1
                else:
                    right = mid

            # 'left' is now the index where x should replace an existing tail,
            # or extend the tails list if x is larger than all current tails.
            
            # Record the predecessor if x is not the first element in a new subsequence
            if left > 0:
                parent[i] = tails_indices[left - 1]

            if left == len(tails_indices):
                tails_indices.append(i)
            else:
                tails_indices[left] = i

        # Reconstruct the sequence starting from the index of the last tail
        sequence = []
        curr = tails_indices[-1]
        while curr != -1:
            sequence.append(arr[curr])
            curr = parent[curr]

        return len(tails_indices), sequence[::-1]