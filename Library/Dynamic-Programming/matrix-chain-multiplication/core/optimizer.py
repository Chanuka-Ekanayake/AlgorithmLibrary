from typing import List, Tuple, Any

class MatrixChainOptimizer:
    """
    Implements the Matrix Chain Multiplication algorithm using 
    Dynamic Programming to find the most efficient way to multiply 
    a given sequence of matrices.
    """

    @staticmethod
    def optimize_multiplication_order(dimensions: List[int]) -> Tuple[int, str]:
        """
        Computes the minimum number of scalar multiplications needed 
        to multiply a chain of matrices, and the optimal parenthesization.
        
        Args:
            dimensions: A list `p` where matrix $A_i$ has dimension $p[i-1] \\times p[i]$.
                        The length of the list is n + 1 where n is the number of matrices.
                        
        Returns:
            A tuple containing:
            - The minimum number of scalar multiplications (int)
            - The optimal parenthesization as a string (e.g., "((A1A2)A3)")
            
        Time Complexity: O(n^3)
        Space Complexity: O(n^2)
        """
        n = len(dimensions) - 1
        if n <= 0:
            return 0, ""

        # dp[i][j] stores the minimum number of multiplications needed for A_i...A_j
        dp = [[0] * (n + 1) for _ in range(n + 1)]
        # split[i][j] stores the index k that achieves the optimal split
        split = [[0] * (n + 1) for _ in range(n + 1)]

        # L is the chain length
        for L in range(2, n + 1):
            for i in range(1, n - L + 2):
                j = i + L - 1
                dp[i][j] = int('inf')
                for k in range(i, j):
                    # q is the cost of multiplying A_i...A_k and A_{k+1}...A_j
                    q = dp[i][k] + dp[k + 1][j] + dimensions[i - 1] * dimensions[k] * dimensions[j]
                    if q < dp[i][j]:
                        dp[i][j] = q
                        split[i][j] = k

        def _construct_optimal_parens(s: List[List[int]], i: int, j: int) -> str:
            if i == j:
                return f"A{i}"
            else:
                return f"({_construct_optimal_parens(s, i, s[i][j])}{_construct_optimal_parens(s, s[i][j] + 1, j)})"

        optimal_parens = _construct_optimal_parens(split, 1, n)
        return dp[1][n], optimal_parens
