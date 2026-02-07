import sys
import random
import uuid
from pathlib import Path

# Add parent directory to path for core logic access
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

try:
    from core.hll import HyperLogLog
except ImportError:
    print("Error: Ensure 'core/hll.py' and 'core/__init__.py' exist.")
    sys.exit(1)

def run_cardinality_simulation():
    print("--------------------------------------------------")
    print("SYSTEM: UNIQUE VISITOR SIMULATOR")
    print("ALGORITHM: HYPERLOGLOG (PROBABILISTIC COUNTING)")
    print("--------------------------------------------------\n")

    # Configuration
    TRUE_UNIQUE_COUNT = 50000
    TOTAL_REQUESTS = 150000  # Includes repeat visitors
    
    # 1. Generate a pool of unique User IDs (UUIDs)
    print(f"[GENERATE] Creating {TRUE_UNIQUE_COUNT} unique user IDs...")
    user_pool = [str(uuid.uuid4()) for _ in range(TRUE_UNIQUE_COUNT)]

    # 2. Initialize exact and probabilistic counters
    exact_set = set()
    hll = HyperLogLog(precision=12) # ~1.6% error rate, ~3KB memory

    print(f"[SIMULATE] Processing {TOTAL_REQUESTS} total visit requests...")
    
    for i in range(TOTAL_REQUESTS):
        # Pick a random user from our pool (creates repeat visits)
        user_id = random.choice(user_pool)
        
        exact_set.add(user_id)
        hll.add(user_id)
        
        if (i + 1) % 50000 == 0:
            print(f"  Processed {i + 1} requests...")

    # 3. Results Comparison
    actual = len(exact_set)
    estimate = hll.count()
    error_percent = abs(actual - estimate) / actual * 100

    # Memory Calculation (Simplified)
    # Average UUID string is ~36 chars (36 bytes) + Python set overhead
    set_memory_kb = (actual * 64) / 1024  # Rough estimate: 64 bytes per entry
    hll_memory_kb = hll.m / 1024         # 1 byte per register

    print("\n" + "="*50)
    print("FINAL AUDIT REPORT")
    print("="*50)
    print(f"Total Requests Handled: {TOTAL_REQUESTS:,}")
    print(f"Actual Unique Users:   {actual:,}")
    print(f"HLL Estimated Users:   {estimate:,}")
    print(f"Estimation Error:      {error_percent:.2f}%")
    print("-" * 50)
    print(f"Python Set Memory:     ~{set_memory_kb:,.2f} KB")
    print(f"HyperLogLog Memory:    ~{hll_memory_kb:,.2f} KB")
    print("-" * 50)
    
    improvement = set_memory_kb / hll_memory_kb
    print(f"RESULT: HLL is {improvement:.0f}x more memory efficient.")
    print("--------------------------------------------------")

if __name__ == "__main__":
    run_cardinality_simulation()