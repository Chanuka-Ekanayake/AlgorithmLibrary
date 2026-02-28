import sys
import time
import random
from pathlib import Path

# Add parent directory for core logic
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

try:
    from core.bit import FenwickTree
except ImportError:
    print("Error: Ensure 'core/bit.py' and 'core/__init__.py' exist.")
    sys.exit(1)

def run_analytics_simulator():
    print("-" * 65)
    print("SYSTEM: REAL-TIME SALES ANALYTICS DASHBOARD")
    print("ENGINE: FENWICK TREE (BINARY INDEXED TREE)")
    print("-" * 65 + "\n")

    # 1. Simulate Historical Data (1 Year of Daily Revenue)
    days_in_year = 365
    print(f"[DATA] Loading historical revenue for {days_in_year} days...")
    
    # Generate random daily revenue between $1,000 and $5,000
    historical_sales = [round(random.uniform(1000, 5000), 2) for _ in range(days_in_year)]
    
    # 2. O(N) Bulk Initialization
    print("[PROCESSING] Building Fenwick Tree in O(N) time...")
    start_build = time.perf_counter()
    sales_tree = FenwickTree.build_from_array(historical_sales)
    end_build = time.perf_counter()
    
    print(f"         Tree built in {(end_build - start_build) * 1000:.4f} ms.\n")

    # 3. Live Dashboard Queries (O(log N))
    print("=" * 65)
    print("DASHBOARD METRICS (Pre-Update)")
    print("=" * 65)
    
    # Q1: Days 1 to 90
    q1_revenue = sales_tree.query_range(1, 90)
    print(f"Q1 Revenue (Days 1-90):      ${q1_revenue:,.2f}")
    
    # Q2: Days 91 to 181
    q2_revenue = sales_tree.query_range(91, 181)
    print(f"Q2 Revenue (Days 91-181):    ${q2_revenue:,.2f}")
    
    # YTD: Days 1 to 365
    ytd_revenue = sales_tree.query_prefix(365)
    print(f"YTD Total Revenue:           ${ytd_revenue:,.2f}\n")

    # 4. Simulating Live High-Frequency Updates
    print("[LIVE] Processing incoming real-time transactions...")
    
    # Let's say today is Day 365. 5 new massive software licenses are sold.
    live_transactions = [15000.00, 22500.50, 8900.00, 12000.00, 45000.00]
    
    start_update = time.perf_counter()
    for tx in live_transactions:
        # Update Day 365's total in O(log N) time
        sales_tree.add(365, tx)
    end_update = time.perf_counter()

    print(f"[SUCCESS] 5 transactions processed in {(end_update - start_update) * 1000:.4f} ms.\n")

    # 5. Live Dashboard Queries (Post-Update)
    print("=" * 65)
    print("DASHBOARD METRICS (Post-Update)")
    print("=" * 65)
    
    # Notice we don't need to recalculate the whole array. We just query again.
    new_ytd_revenue = sales_tree.query_prefix(365)
    print(f"Updated YTD Revenue:         ${new_ytd_revenue:,.2f}")
    
    # Verify the exact difference
    difference = new_ytd_revenue - ytd_revenue
    expected = sum(live_transactions)
    print("-" * 65)
    print(f"Delta Captured: ${difference:,.2f} (Expected: ${expected:,.2f})")
    print("=" * 65)

if __name__ == "__main__":
    run_analytics_simulator()