"""
Burrows-Wheeler Transform (BWT)
A reversible string transformation algorithm used heavily in data compression 
(like bzip2) and bioinformatics. It rearranges strings into runs of similar 
characters, preparing them for highly efficient entropy encoding.
"""

from typing import List, Tuple

class BurrowsWheeler:
    """
    Data transformation engine for advanced compression pipelines.
    """
    
    # A unique End-Of-File marker. It must be a character that 
    # mathematically guarantees it is not present in the input text.
    EOF = "$"

    @classmethod
    def transform(cls, text: str) -> str:
        """
        Forward BWT: Generates the transformed string.
        
        Args:
            text: The original string to be transformed.
            
        Returns:
            The BWT string, where identical characters are often grouped.
        """
        if cls.EOF in text:
            raise ValueError(f"Input text cannot contain the reserved EOF marker: '{cls.EOF}'")
            
        # Append the EOF marker to strictly define the end of the sequence
        text += cls.EOF
        n = len(text)
        
        # 1. Generate all cyclic permutations (rotations) of the string.
        # Note: In production, we use Suffix Arrays here to achieve O(N) time.
        # For this implementation, we use Python's slicing for clarity.
        rotations = [text[i:] + text[:i] for i in range(n)]
        
        # 2. Sort the rotations lexicographically (alphabetically)
        rotations.sort()
        
        # 3. Extract the last column (the Last array, or 'L')
        bwt_string = "".join(rotation[-1] for rotation in rotations)
        
        return bwt_string

    @classmethod
    def inverse(cls, bwt_string: str) -> str:
        """
        Inverse BWT: Reconstructs the original text in O(N) time using LF Mapping.
        
        Args:
            bwt_string: The transformed string (the 'L' column).
            
        Returns:
            The original, uncompressed string.
        """
        if not bwt_string:
            return ""

        n = len(bwt_string)
        
        # 1. The 'L' array is our input (Last column)
        L = list(bwt_string)
        
        # 2. The 'F' array (First column) is simply the sorted version of 'L'
        F = sorted(L)
        
        # 3. Build the LF Mapping (Last-to-First)
        # We need to map the i-th occurrence of a character in L to the 
        # i-th occurrence of that same character in F.
        
        # Tally arrays to track the occurrence count of each character as we iterate
        l_counts = {}
        f_counts = {}
        
        # Store tuples of (character, occurrence_id)
        # Example: The second 'a' in the string becomes ('a', 1)
        L_indexed: List[Tuple[str, int]] = []
        F_indexed: List[Tuple[str, int]] = []
        
        for i in range(n):
            # Process L
            char_l = L[i]
            count_l = l_counts.get(char_l, 0)
            L_indexed.append((char_l, count_l))
            l_counts[char_l] = count_l + 1
            
            # Process F
            char_f = F[i]
            count_f = f_counts.get(char_f, 0)
            F_indexed.append((char_f, count_f))
            f_counts[char_f] = count_f + 1

        # Build a dictionary to map the (character, occurrence_id) from L to its index in L
        # This allows us to jump from F back to L instantly.
        l_lookup = {item: index for index, item in enumerate(L_indexed)}

        # 4. Reconstruct the original string
        # We start at the EOF character in the First column
        current_item = (cls.EOF, 0)
        original_string = []
        
        # We traverse exactly N times to rebuild the string backwards
        for _ in range(n):
            # Find where this specific character instance lives in the Last column
            next_index = l_lookup[current_item]
            
            # The character in the First column at 'next_index' is the preceding character
            current_item = F_indexed[next_index]
            
            # We skip appending the EOF marker to the final output
            if current_item[0] != cls.EOF:
                original_string.append(current_item[0])

        # Because we walked the LF mapping, we built the string in reverse.
        return "".join(reversed(original_string))