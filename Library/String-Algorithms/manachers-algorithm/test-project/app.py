import sys
import time
from pathlib import Path

# Add parent directory for core logic
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

try:
    from core.manacher import Manacher
except ImportError:
    print("Error: Ensure 'core/manacher.py' and 'core/__init__.py' exist.")
    sys.exit(1)

def run_genomic_scanner():
    print("-" * 65)
    print("SYSTEM: GENOMIC PALINDROME SCANNER")
    print("ALGORITHM: MANACHER'S ALGORITHM O(N)")
    print("-" * 65 + "\n")

    # 1. Simulated Genomic Sequence
    # Hidden inside this sequence is a long palindrome: "GATTACA...ACATTAG"
    dna_sequence = (
        "ACGTACGTACGT"
        "GATTACACATTAG"  # Palindrome (length 13)
        "CGTACGTACGTAC"
        "TGGATCCAT"      # Palindrome (length 9)
        "CGTAC"
    )

    print(f"[DATA] Scanning {len(dna_sequence)} base pairs of DNA...")
    print("[PROCESSING] Injecting sentinels and executing O(N) linear scan...\n")

    # 2. Execute Manacher's Algorithm
    start_time = time.perf_counter()
    longest_palindrome = Manacher.find_longest_palindrome(dna_sequence)
    end_time = time.perf_counter()

    # 3. Results Output
    print("="*65)
    print("SCAN REPORT")
    print("="*65)
    print(f"Longest Palindromic Sequence: {longest_palindrome}")
    print(f"Sequence Length:              {len(longest_palindrome)} base pairs")
    
    # Verify we extracted the exact sequence and not a preprocessed string
    assert "#" not in longest_palindrome, "CRITICAL ERROR: Preprocessing characters leaked into output."

    print("-" * 65)
    print(f"Execution Time: {(end_time - start_time) * 1000:.4f} ms")
    print("="*65)
    print("RESULT: Symmetrical genomic structure extracted in linear time.")

if __name__ == "__main__":
    run_genomic_scanner()