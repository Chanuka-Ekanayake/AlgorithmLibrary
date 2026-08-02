def needleman_wunsch(seq1, seq2, match_score=1, mismatch_score=-1, gap_penalty=-1):
    """
    Computes the optimal global alignment of two sequences using the Needleman-Wunsch algorithm.
    """
    m, n = len(seq1), len(seq2)
    
    # Initialize the scoring matrix
    score_matrix = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
    
    # Initialization
    for i in range(m + 1):
        score_matrix[i][0] = i * gap_penalty
    for j in range(n + 1):
        score_matrix[0][j] = j * gap_penalty
        
    # Matrix filling
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if seq1[i - 1] == seq2[j - 1]:
                match = score_matrix[i - 1][j - 1] + match_score
            else:
                match = score_matrix[i - 1][j - 1] + mismatch_score
            delete = score_matrix[i - 1][j] + gap_penalty
            insert = score_matrix[i][j - 1] + gap_penalty
            score_matrix[i][j] = max(match, delete, insert)
            
    # Traceback
    align1, align2 = "", ""
    i, j = m, n
    
    while i > 0 and j > 0:
        score_current = score_matrix[i][j]
        score_diagonal = score_matrix[i - 1][j - 1]
        score_up = score_matrix[i - 1][j]
        score_left = score_matrix[i][j - 1]
        
        if score_current == score_diagonal + (match_score if seq1[i - 1] == seq2[j - 1] else mismatch_score):
            align1 += seq1[i - 1]
            align2 += seq2[j - 1]
            i -= 1
            j -= 1
        elif score_current == score_left + gap_penalty:
            align1 += "-"
            align2 += seq2[j - 1]
            j -= 1
        elif score_current == score_up + gap_penalty:
            align1 += seq1[i - 1]
            align2 += "-"
            i -= 1
            
    # Finish tracing back to the top-left cell
    while i > 0:
        align1 += seq1[i - 1]
        align2 += "-"
        i -= 1
    while j > 0:
        align1 += "-"
        align2 += seq2[j - 1]
        j -= 1
        
    return align1[::-1], align2[::-1], score_matrix[m][n]

if __name__ == "__main__":
    seq1 = "GATTACA"
    seq2 = "GCATGCU"
    
    print("--- Needleman-Wunsch Algorithm ---")
    print(f"Sequence 1: {seq1}")
    print(f"Sequence 2: {seq2}")
    
    a1, a2, score = needleman_wunsch(seq1, seq2)
    
    print("\nOptimal Alignment:")
    print(a1)
    print(a2)
    print(f"Alignment Score: {score}")
