"""
Z-Algorithm - Linear Time Pattern Matching
Efficiently finds all occurrences of a pattern in a text using 
Z-array construction and 'Z-box' windowing.
"""

from typing import List

def compute_z(s: str) -> List[int]:
    """
    Computes the Z-array for string s.
    Z[i] is the length of the longest substring starting from s[i]
    which is also a prefix of s.
    """
    n = len(s)
    z = [0] * n
    # [l, r] make a window (Z-box) which matches the prefix
    l, r = 0, 0
    
    for i in range(1, n):
        # Case 1: i is outside the current Z-box
        if i > r:
            l, r = i, i
            while r < n and s[r - l] == s[r]:
                r += 1
            z[i] = r - l
            r -= 1
        # Case 2: i is inside the current Z-box
        else:
            k = i - l
            # Case 2a: The previously computed Z-value fits inside the box
            if z[k] < r - i + 1:
                z[i] = z[k]
            # Case 2b: The match might extend beyond the box
            else:
                l = i
                while r < n and s[r - l] == s[r]:
                    r += 1
                z[i] = r - l
                r -= 1
    return z

def z_search(text: str, pattern: str) -> List[int]:
    """
    Finds all 0-indexed starting positions of pattern in text.
    Uses the 'concatenation trick' to achieve O(n + m) matching.
    """
    if not pattern or not text:
        return []
        
    # Standard concatenation: pattern + sentinel + text
    # The sentinel '$' must not appear in the pattern or text
    combined = pattern + "$" + text
    z = compute_z(combined)
    
    pattern_len = len(pattern)
    matches = []
    
    # Iterate through the portion of Z-array corresponding to 'text'
    # Start after pattern length + 1 (the sentinel)
    for i in range(pattern_len + 1, len(z)):
        if z[i] == pattern_len:
            # Shift index back to the original text coordinate
            matches.append(i - pattern_len - 1)
            
    return matches