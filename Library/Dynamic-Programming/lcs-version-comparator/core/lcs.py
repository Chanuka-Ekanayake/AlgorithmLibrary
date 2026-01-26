from typing import List, Any

class VersionComparator:
    """
    Implements the Longest Common Subsequence (LCS) algorithm using 
    Dynamic Programming to identify similarities between data sequences.
    """

    @staticmethod
    def get_lcs(sequence_a: List[Any], sequence_b: List[Any]) -> List[Any]:
        """
        Computes the Longest Common Subsequence of two sequences.
        Time Complexity: O(m * n)
        Space Complexity: O(m * n)
        """
        m = len(sequence_a)
        n = len(sequence_b)

        # Initialize the DP table with zeros
        # dp[i][j] stores the length of LCS of sequence_a[0...i-1] and sequence_b[0...j-1]
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        # Build the tabulation matrix
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if sequence_a[i - 1] == sequence_b[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        # Backtrack to reconstruct the subsequence
        lcs = []
        i, j = m, n
        while i > 0 and j > 0:
            if sequence_a[i - 1] == sequence_b[j - 1]:
                lcs.append(sequence_a[i - 1])
                i -= 1
                j -= 1
            elif dp[i - 1][j] > dp[i][j - 1]:
                i -= 1
            else:
                j -= 1

        return lcs[::-1]  # Return the reversed list for correct order

    @staticmethod
    def calculate_similarity(sequence_a: List[Any], sequence_b: List[Any]) -> float:
        """
        Calculates the similarity percentage between two sequences 
        based on their Longest Common Subsequence.
        """
        lcs_length = len(VersionComparator.get_lcs(sequence_a, sequence_b))
        max_length = max(len(sequence_a), len(sequence_b))
        
        if max_length == 0:
            return 100.0
            
        return (lcs_length / max_length) * 100