import sys
import time
import os

# Add parent directory for core logic
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

try:
    from core.lis import LongestIncreasingSubsequence
except ImportError:
    print("Error: Ensure 'core/lis.py' and 'core/__init__.py' exist.")
    sys.exit(1)

def run_stock_analyzer():
    print("-" * 65)
    print("SYSTEM: STOCK TREND ANALYZER")
    print("ALGORITHM: LONGEST INCREASING SUBSEQUENCE (LIS)")
    print("-" * 65 + "\n")

    # 1. Simulated 30-day volatile stock prices
    stock_prices = [
        120, 118, 122, 119, 125, 130, 128, 126, 135, 133, 
        132, 140, 138, 142, 145, 144, 150, 148, 149, 155, 
        152, 160, 158, 162, 165, 163, 170, 168, 172, 175
    ]

    print("[DATA] 30-Day Price History:")
    print(f"{stock_prices}\n")

    analyzer = LongestIncreasingSubsequence()

    # 2. Run Classic DP
    print("[PROCESSING] Running Classic DP O(N^2)...")
    start_dp = time.perf_counter()
    len_dp, seq_dp = analyzer.classic_dp(stock_prices)
    end_dp = time.perf_counter()
    
    # 3. Run Optimal Binary Search
    print("[PROCESSING] Running Binary Search O(N log N)...")
    start_bs = time.perf_counter()
    len_bs, seq_bs = analyzer.optimal_binary_search(stock_prices)
    end_bs = time.perf_counter()

    # 4. Results Validation
    assert len_dp == len_bs and seq_dp == seq_bs, "CRITICAL ERROR: Algorithm mismatch."

    print("\n" + "="*65)
    print("TREND ANALYSIS REPORT")
    print("="*65)
    print(f"Max Upward Trend Length: {len_bs} strictly increasing price points")
    print(f"Trend Sequence (Prices): {seq_bs}")
    print("-" * 65)
    print("PERFORMANCE METRICS:")
    print(f"Classic DP Time:       {(end_dp - start_dp) * 1000:.4f} ms")
    print(f"Binary Search Time:    {(end_bs - start_bs) * 1000:.4f} ms")
    print("="*65)
    print("RESULT: Both methods verified. Data successfully extracted.")

if __name__ == "__main__":
    run_stock_analyzer()