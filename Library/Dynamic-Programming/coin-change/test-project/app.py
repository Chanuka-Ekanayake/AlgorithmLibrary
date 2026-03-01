import sys
import time
from pathlib import Path

# Add parent directory for core logic
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

try:
    from core.optimizer import ResourceOptimizer
except ImportError:
    print("Error: Ensure 'core/optimizer.py' and 'core/__init__.py' exist.")
    sys.exit(1)

def greedy_allocation(bundles: list[int], target: int) -> list[int]:
    """
    A naive Greedy approach: Always pick the largest possible bundle first.
    """
    sorted_bundles = sorted(bundles, reverse=True)
    allocation = []
    remaining = target
    
    for bundle in sorted_bundles:
        while remaining >= bundle:
            allocation.append(bundle)
            remaining -= bundle
            
    # If remaining > 0 at the end, the greedy approach failed to hit the exact target
    return allocation if remaining == 0 else []

def run_allocation_simulator():
    print("-" * 65)
    print("SYSTEM: API CREDIT BUNDLE ALLOCATION")
    print("ENGINE: DYNAMIC PROGRAMMING VS. GREEDY")
    print("-" * 65 + "\n")

    # 1. Define Pricing Tiers & Target
    # We sell API credits in bundles of 100, 1500, and 2500.
    available_bundles = [100, 1500, 2500]
    
    # A user wants to buy exactly 3000 compute credits.
    target_credits = 3000

    print(f"[STORE] Available Credit Bundles: {available_bundles}")
    print(f"[ORDER] User requested exact allocation of: {target_credits} credits\n")

    # 2. Execute Naive Greedy Algorithm
    print("[PROCESSING] Running Naive Greedy Allocator...")
    start_greedy = time.perf_counter()
    greedy_receipt = greedy_allocation(available_bundles, target_credits)
    end_greedy = time.perf_counter()
    
    # 3. Execute DP Optimizer
    print("[PROCESSING] Running Dynamic Programming Engine...")
    start_dp = time.perf_counter()
    try:
        dp_receipt = ResourceOptimizer.get_optimal_allocation(available_bundles, target_credits)
    except ValueError as exc:
        end_dp = time.perf_counter()
        print(f"[ERROR] Dynamic Programming Engine could not fulfill the exact target: {exc}")
        dp_receipt = []
    else:
        end_dp = time.perf_counter()

    # 4. Output Results & Comparison
    print("\n" + "=" * 65)
    print("ALLOCATION RECEIPT COMPARISON")
    print("=" * 65)
    
    print("1. GREEDY ALGORITHM RESULT:")
    if greedy_receipt:
        print(f"   Bundles Used: {len(greedy_receipt)}")
        print(f"   Allocation:   {greedy_receipt}")
        print("   Logic: Picked 2500 once, then fell back to 100 five times.")
    else:
        print("   FAILED: Could not fulfill exact amount.")
        
    print("-" * 65)
    
    print("2. DYNAMIC PROGRAMMING RESULT:")
    if dp_receipt:
        print(f"   Bundles Used: {len(dp_receipt)}  <-- (MATHEMATICAL OPTIMUM)")
        print(f"   Allocation:   {dp_receipt}")
        print("   Logic: Identified overlapping subproblem (1500 + 1500).")
    else:
        print("   FAILED: Could not fulfill exact amount.")

    print("=" * 65)
    
    # 5. Performance Metrics
    overhead_saved = len(greedy_receipt) - len(dp_receipt)
    print(f"[METRIC] DP Engine saved {overhead_saved} unnecessary database allocations.")
    print(f"[METRIC] Greedy Exec Time: {(end_greedy - start_greedy) * 1000:.4f} ms")
    print(f"[METRIC] DP Exec Time:     {(end_dp - start_dp) * 1000:.4f} ms")
    print("=" * 65)

if __name__ == "__main__":
    run_allocation_simulator()