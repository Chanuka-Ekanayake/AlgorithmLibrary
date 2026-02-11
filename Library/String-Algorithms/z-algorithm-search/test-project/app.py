import sys
from pathlib import Path

# Add parent directory to path for core logic access
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

try:
    from core.z_search import z_search
except ImportError:
    print("Error: Ensure 'core/z_search.py' and 'core/__init__.py' exist.")
    sys.exit(1)

def run_code_search_sim():
    print("--------------------------------------------------")
    print("SYSTEM: DEEP CODE SEARCH SIMULATOR")
    print("ALGORITHM: Z-ALGORITHM (LINEAR STRING MATCH)")
    print("--------------------------------------------------\n")

    # 1. Simulated codebase (Repetitive structure to challenge naive search)
    codebase = (
        "def test_model_v1():\n    return 'success'\n" * 50 +
        "def calculate_loss(y_true, y_pred):\n    return sum((y_true - y_pred)**2)\n" +
        "def test_model_v2():\n    return 'success'\n" * 50 +
        "def calculate_loss(y_true, y_pred):\n    # Optimized version\n    return np.mean(np.square(y_true - y_pred))\n"
    )

    # 2. Search Pattern
    pattern = "def calculate_loss"
    
    print(f"[SEARCHING] Looking for pattern: '{pattern}'")
    print(f"[METADATA] Codebase size: {len(codebase)} characters")
    
    # 3. Execute Z-Search
    matches = z_search(codebase, pattern)
    
    # 4. Display Results
    if matches:
        print(f"\n✨ [FOUND] {len(matches)} occurrences found in linear time:")
        print("-" * 50)
        for i, pos in enumerate(matches):
            # Extract a snippet for visualization
            snippet = codebase[pos:pos+60].replace('\n', ' ')
            print(f"Match {i+1} at index {pos:05d}: {snippet}...")
    else:
        print("\n[INFO] No matches found.")

    print("\n" + "-"*50)
    print("STATUS: SEARCH COMPLETE")
    print("--------------------------------------------------")

if __name__ == "__main__":
    run_code_search_sim()