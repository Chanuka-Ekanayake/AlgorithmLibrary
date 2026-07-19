def get_bad_char_table(pattern: str) -> dict:
    """
    Creates the bad character heuristic table for the Boyer-Moore algorithm.
    """
    bad_char_table = {}
    pattern_length = len(pattern)
    for i in range(pattern_length):
        bad_char_table[pattern[i]] = i
    return bad_char_table

def search(text: str, pattern: str) -> list[int]:
    """
    Searches for all occurrences of the pattern in the text using 
    the Boyer-Moore Bad Character Heuristic.
    Returns a list of starting indices where the pattern is found.
    """
    occurrences = []
    m = len(pattern)
    n = len(text)
    
    if m == 0:
        return []
        
    bad_char_table = get_bad_char_table(pattern)
    
    # s is the shift of the pattern with respect to text
    s = 0 
    while s <= (n - m):
        j = m - 1
        
        # Keep reducing index j of pattern while characters of pattern and text are matching at this shift s
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
            
        # If the pattern is present at current shift, then index j will become -1 after the above loop
        if j < 0:
            occurrences.append(s)
            
            # Shift the pattern so that the next character in text aligns with the last occurrence of it in pattern.
            # The condition s + m < n is necessary for the case when pattern occurs at the end of text
            if s + m < n:
                s += (m - bad_char_table.get(text[s + m], -1))
            else:
                s += 1
        else:
            # Shift the pattern so that the bad character in text aligns with the last occurrence of it in pattern.
            # The max function is used to make sure that we get a positive shift. We may get a negative shift 
            # if the last occurrence of bad character in pattern is on the right side of the current character.
            s += max(1, j - bad_char_table.get(text[s + j], -1))
            
    return occurrences
