"""
Knuth-Morris-Pratt (KMP) Pattern Matching
An efficient O(N + M) string searching algorithm that uses 
an LPS (Longest Prefix Suffix) array to avoid re-evaluating 
previously matched characters.
"""

from typing import List

class KMPMatcher:
    """
    Executes advanced pattern matching on text strings.
    """

    @staticmethod
    def compute_lps_array(pattern: str) -> List[int]:
        """
        Pre-processes the pattern to create the LPS array.
        lps[i] holds the length of the longest proper prefix 
        that is also a suffix in pattern[0..i].
        """
        m = len(pattern)
        lps = [0] * m
        
        # 'length' tracks the length of the previous longest prefix suffix
        length = 0 
        i = 1

        while i < m:
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                # If there is a mismatch, we don't increment i immediately.
                # Instead, we fall back to the previous valid prefix length.
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
                    
        return lps

    @staticmethod
    def search(text: str, pattern: str) -> List[int]:
        """
        Searches for all occurrences of 'pattern' in 'text'.
        Time Complexity: O(N + M)
        
        Returns:
            A list of starting indices where the pattern is found.
        """
        n = len(text)
        m = len(pattern)
        
        if m == 0:
            return []

        # 1. Preprocess the pattern
        lps = KMPMatcher.compute_lps_array(pattern)
        
        indices = []
        i = 0  # index for text
        j = 0  # index for pattern

        # 2. Execute the search
        while i < n:
            if pattern[j] == text[i]:
                i += 1
                j += 1

            if j == m:
                # A full match is found! Record the starting index.
                indices.append(i - j)
                # Fall back using the LPS array to continue searching
                j = lps[j - 1]
                
            elif i < n and pattern[j] != text[i]:
                # Mismatch after j matches
                if j != 0:
                    # Do not match lps[0..lps[j-1]] characters, 
                    # they will match anyway
                    j = lps[j - 1]
                else:
                    i += 1

        return indices