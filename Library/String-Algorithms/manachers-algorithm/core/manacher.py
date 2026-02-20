"""
Manacher's Algorithm
Finds the Longest Palindromic Substring in strict O(N) time.
Utilizes dynamic programming to mirror previously computed palindrome 
radii, avoiding redundant character comparisons.
"""

class Manacher:
    """
    Executes linear-time palindrome extraction using center boundaries.
    """

    @staticmethod
    def _preprocess(s: str) -> str:
        """
        Injects boundaries to uniformly handle even and odd length palindromes.
        Adds '^' and '$' at the ends to act as natural sentinels, eliminating 
        the need for bounds checking during the while loop expansion.
        
        Example: "aba" -> "^#a#b#a#$"
        """
        if not s:
            return "^$"
        
        return "^#" + "#".join(s) + "#$"

    @staticmethod
    def find_longest_palindrome(s: str) -> str:
        """
        Extracts the longest palindromic substring from the input string.
        Time Complexity: O(N)
        Space Complexity: O(N)
        
        Args:
            s: The original string to search.
            
        Returns:
            The longest palindromic substring.
        """
        if not s:
            return ""

        # 1. Transform the string
        T = Manacher._preprocess(s)
        n = len(T)
        
        # P[i] stores the radius of the longest palindrome centered at T[i]
        P = [0] * n
        
        C = 0  # Center of the palindrome that extends furthest to the right
        R = 0  # The rightmost boundary of this palindrome

        # 2. Execute the linear scan
        # We start at 1 and end at n-1 to avoid the '^' and '$' sentinels
        for i in range(1, n - 1):
            # Calculate the corresponding mirror index of 'i' relative to center 'C'
            mirror = 2 * C - i

            # If the current index is within the right boundary (R), 
            # we can safely copy the mirror's pre-computed radius to avoid redundant checks.
            # We use min() to ensure we don't accidentally expand past our known safe boundary R.
            if i < R:
                P[i] = min(R - i, P[mirror])

            # 3. Expand the palindrome centered at i
            # Because of the '^' and '$' sentinels, this will never throw an IndexError.
            while T[i + 1 + P[i]] == T[i - 1 - P[i]]:
                P[i] += 1

            # 4. Update the Center and Right Boundary
            # If the palindrome centered at i expands past the current right boundary R,
            # we shift our center to i, and update R.
            if i + P[i] > R:
                C = i
                R = i + P[i]

        # 5. Find the maximum element in P and extract the result
        max_len = 0
        center_index = 0
        for i, radius in enumerate(P):
            if radius > max_len:
                max_len = radius
                center_index = i

        # Calculate the starting index in the original (un-preprocessed) string
        start_index = (center_index - 1 - max_len) // 2
        
        return s[start_index : start_index + max_len]