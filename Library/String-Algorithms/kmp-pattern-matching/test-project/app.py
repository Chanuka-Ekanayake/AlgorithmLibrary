import sys
import time
from pathlib import Path

# Add parent directory for core logic
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

try:
    from core.kmp import KMPMatcher
except ImportError:
    print("Error: Ensure 'core/kmp.py' and 'core/__init__.py' exist.")
    sys.exit(1)

def run_description_scanner():
    print("-" * 65)
    print("SYSTEM: MODEL DESCRIPTION SCANNER")
    print("ALGORITHM: KNUTH-MORRIS-PRATT (KMP) PATTERN MATCHING")
    print("-" * 65 + "\n")

    # 1. Simulated Database Text (e.g., a long ML model description)
    model_description = (
        "This package provides a comprehensive suite for biometric analysis. "
        "It includes tools for liveness detection, spatial analysis, and a "
        "highly optimized face-verification-api. The face-verification-api "
        "is designed for zero-budget deployments, requiring minimal compute. "
        "Developers can integrate the face-verification module easily."
    )
    
    # 2. The Search Query
    search_term = "face-verification"

    print(f"[DATA] Scanning {len(model_description)} characters of text...")
    print(f"[QUERY] Target Pattern: '{search_term}'\n")

    # 3. Execute KMP Search
    print("[PROCESSING] Generating LPS Array and executing O(N+M) search...")
    start_time = time.perf_counter()
    
    # Call the search method directly
    match_indices = KMPMatcher.search(model_description, search_term)
    
    end_time = time.perf_counter()

    # 4. Results Output
    print("\n" + "="*65)
    print("SCAN REPORT")
    print("="*65)
    print(f"Occurrences Found: {len(match_indices)}")
    
    for i, index in enumerate(match_indices, 1):
        # Extract a small snippet around the match for context
        start = max(0, index - 15)
        end = min(len(model_description), index + len(search_term) + 15)
        snippet = model_description[start:end].replace('\n', ' ')
        print(f"Match {i} at Index {index:<4} | Context: \"...{snippet}...\"")

    print("-" * 65)
    print(f"Execution Time: {(end_time - start_time) * 1000:.4f} ms")
    print("="*65)
    print("RESULT: All matches extracted without text backtracking.")

if __name__ == "__main__":
    run_description_scanner()