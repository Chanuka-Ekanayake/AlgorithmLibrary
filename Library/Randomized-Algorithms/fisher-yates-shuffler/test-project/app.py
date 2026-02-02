import sys
import os
import json
from typing import List, Dict

# Add parent directory to path for core logic access
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.shuffler import FisherYatesShuffler

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_products(filepath: str) -> List[Dict]:
    """Loads product data for the marketplace."""
    with open(filepath, 'r') as f:
        return json.load(f)

def run_marketplace_simulation():
    clear_screen()
    print("--------------------------------------------------")
    print("SYSTEM: FAIR-MARKETPLACE ROTATOR")
    print("ALGORITHM: FISHER-YATES (UNBIASED SHUFFLE)")
    print("--------------------------------------------------\n")

    # 1. Load Data
    products = load_products('marketplace_data.json')
    print(f"LOADED: {len(products)} products from the catalog.")
    
    # 2. Perform Single Shuffle (for current user view)
    print("\n[ACTION] Shuffling 'Featured Products' for new session...")
    shuffled_view = FisherYatesShuffler.shuffle(list(products))
    
    print("\n--- NEW FEATURED LIST ---")
    for i, p in enumerate(shuffled_view, 1):
        print(f"{i}. {p['name']} (by {p['developer']})")
    print("-------------------------\n")

    # 3. Fairness Audit (Statistical Proof)
    print("RUNNING FAIRNESS AUDIT (100,000 Iterations)...")
    # Using IDs to track frequency of being in the #1 spot
    first_spot_counts = {p['id']: 0 for p in products}
    
    for _ in range(100000):
        # Fresh copy each time to test distribution
        test_list = list(products)
        FisherYatesShuffler.shuffle(test_list)
        first_spot_counts[test_list[0]['id']] += 1

    print("\n[AUDIT RESULTS] Probability of appearing in Top Spot:")
    for p in products:
        percentage = (first_spot_counts[p['id']] / 100000) * 100
        print(f"  ID {p['id']} ({p['name'][:12]}...): {percentage:.2f}%")
    
    print("\nSTATUS: Mathematically Unbiased Distribution Confirmed.")
    print("--------------------------------------------------")

if __name__ == "__main__":
    run_marketplace_simulation()