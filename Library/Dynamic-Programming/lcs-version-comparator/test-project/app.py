import sys
import os
import json

# Add the parent directory to the path to import the core logic
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.lcs import VersionComparator

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_json_config(filepath):
    """Safely loads a JSON array from a file."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return []

def run_diff_simulation():
    clear_screen()
    print("--------------------------------------------------")
    print("SYSTEM: CONFIGURATION VERSION COMPARATOR")
    print("ALGORITHM: LONGEST COMMON SUBSEQUENCE (LCS)")
    print("--------------------------------------------------\n")

    # Load the sequences
    config_v1 = load_json_config('config_v1.json')
    config_v2 = load_json_config('config_v2.json')

    print(f"File A: config_v1.json ({len(config_v1)} parameters)")
    print(f"File B: config_v2.json ({len(config_v2)} parameters)\n")

    # Execute LCS Logic
    comparator = VersionComparator()
    stable_core = comparator.get_lcs(config_v1, config_v2)
    similarity = comparator.calculate_similarity(config_v1, config_v2)

    # Display Results
    print("IDENTIFIED STABLE CORE (LCS):")
    if stable_core:
        for i, item in enumerate(stable_core, 1):
            print(f"  {i}. {item}")
    else:
        print("  [No common sequence identified]")

    print(f"\nANALYSIS METRICS:")
    print(f"  Similarity Score: {similarity:.2f}%")
    print(f"  Unchanged Count:  {len(stable_core)} parameters")
    
    # Logic Explanation
    print("\nENGINEERING NOTE:")
    print("The LCS identifies the longest sequence of settings that were ")
    print("preserved in their original relative order. Items not listed ")
    print("above represent modified or newly injected parameters.")
    print("--------------------------------------------------")

if __name__ == "__main__":
    run_diff_simulation()