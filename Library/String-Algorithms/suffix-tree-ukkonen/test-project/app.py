import sys
import os

# Add core to path so we can import SuffixTree
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.suffix_tree import SuffixTree

def run_test_cases():
    test_cases = [
        ("BANANA", "ANA", True),
        ("BANANA", "NAN", True),
        ("BANANA", "BAN", True),
        ("BANANA", "APPLE", False),
        ("MISSISSIPPI", "ISSIP", True),
        ("MISSISSIPPI", "IPPI", True),
        ("MISSISSIPPI", "ISSISSIP", True),
        ("MISSISSIPPI", "MISS", True),
        ("GATAGACA", "GATA", True),
        ("GATAGACA", "TAGA", True),
        ("GATAGACA", "GACA", True)
    ]
    
    print("\n" + "="*50)
    print(" Suffix Tree (Ukkonen's) - Test Suite ")
    print("="*50 + "\n")
    
    for text, pattern, expected in test_cases:
        tree = SuffixTree(text)
        result = tree.search(pattern)
        status = "PASSED" if result == expected else "FAILED"
        print(f"[{status}] Text: '{text}' | Pattern: '{pattern}' | Expected: {expected} | Got: {result}")

    print("\n" + "="*50)
    print(" Advanced Search Example ")
    print("="*50)
    
    dna_seq = "ATGCATGCATGCATGC"
    pattern = "CATG"
    tree = SuffixTree(dna_seq)
    
    print(f"\nSearching for '{pattern}' in DNA sequence: {dna_seq}")
    if tree.search(pattern):
        print(f"[FOUND] Pattern '{pattern}' is present in the sequence.")
    else:
        print(f"[NOT FOUND] Pattern '{pattern}' not found.")

if __name__ == "__main__":
    run_test_cases()
