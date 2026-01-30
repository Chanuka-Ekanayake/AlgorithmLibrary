"""
Rabin-Karp String Matching Engine
Uses a polynomial rolling hash to find patterns in text in linear time.
Ideal for plagiarism detection and multiple pattern matching.
"""

from typing import List

class RabinKarp:
    """
    Rabin-Karp implementation using rolling hash.
    
    Attributes:
        d (int): The number of characters in the input alphabet (default 256 for ASCII).
        q (int): A large prime number used for the modulo operation to prevent overflow 
                 and minimize collisions.
    """
    
    def __init__(self, alphabet_size: int = 256, prime: int = 10**9 + 7):
        self.d = alphabet_size
        self.q = prime

    def search(self, pattern: str, text: str) -> List[int]:
        """
        Searches for all occurrences of 'pattern' within 'text'.
        
        Args:
            pattern: The string signature to search for.
            text: The body of text (source code, document) to scan.
            
        Returns:
            A list of starting indices where the pattern was found.
        """
        m = len(pattern)
        n = len(text)
        
        if m == 0 or m > n:
            return []

        results = []
        p_hash = 0  # Hash value for the pattern
        t_hash = 0  # Hash value for the current window in text
        h = 1       # The value of d^(m-1) % q

        # The value of h is used to remove the leading digit of the rolling hash
        # h = pow(d, m-1) % q
        for i in range(m - 1):
            h = (h * self.d) % self.q

        # 1. Pre-calculate the hash of the pattern and the first window of the text
        for i in range(m):
            p_hash = (self.d * p_hash + ord(pattern[i])) % self.q
            t_hash = (self.d * t_hash + ord(text[i])) % self.q

        # 2. Slide the pattern over the text
        for i in range(n - m + 1):
            # If the hash values match, check the actual characters (handle collisions)
            if p_hash == t_hash:
                if text[i : i + m] == pattern:
                    results.append(i)

            # 3. Calculate the hash for the next window
            # Remove the leading digit and add the trailing digit
            if i < n - m:
                # Rolling hash formula: 
                # next_hash = (d * (current_hash - leading_digit * h) + trailing_digit) % q
                t_hash = (self.d * (t_hash - ord(text[i]) * h) + ord(text[i + m])) % self.q
                
                # Ensure the hash is positive
                if t_hash < 0:
                    t_hash += self.q
                    
        return results

    def batch_search(self, patterns: List[str], text: str) -> dict:
        """
        Scans text for multiple patterns simultaneously.
        Useful for malware signature scanning or plagiarism checks.
        """
        scan_results = {}
        for pattern in patterns:
            occurrences = self.search(pattern, text)
            if occurrences:
                scan_results[pattern] = occurrences
        return scan_results