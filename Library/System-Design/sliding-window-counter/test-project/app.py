import os
import sys
import time
from pathlib import Path

# Add parent directory to path for core logic access
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

from core.rate_limiter import RateLimitManager, SlidingWindowCounter

def print_status(counter: SlidingWindowCounter, label: str):
    estimated, curr, prev = counter.get_status()
    print(f"   [STATS] {label:<25} | Estimated: {estimated:.2f} | Current: {curr} | Previous: {prev}")

def simulate_request(manager: RateLimitManager, user_id: str, request_num: int) -> bool:
    allowed = manager.is_allowed(user_id)
    status = "200 OK" if allowed else "429 TOO MANY REQUESTS"
    prefix = "[ALLOW]" if allowed else "[BLOCK]"
    print(f"   {prefix} Request #{request_num:02d}: {status}")
    return allowed

def run_rate_limit_simulation():
    print("==================================================")
    print("SHIELD ENGINE: API Endpoint Rate Limiter")
    print("ALGORITHM: Sliding Window Counter (Weighted)")
    print("==================================================\n")

    # Limit = 5 requests per 10 seconds
    limit = 5
    window_size = 10.0
    manager = RateLimitManager(default_limit=limit, default_window_size=window_size)
    user_id = "Client-Alpha"
    
    # Get the raw counter for printing stats
    counter = manager.buckets.setdefault(user_id, SlidingWindowCounter(limit, window_size))

    print(f"[INIT] Limiting {user_id} to {limit} requests per {int(window_size)}s window.\n")
    print_status(counter, "Initial State")

    print("\nSCENARIO 1: Rapid Spam Attack")
    print("Strategy: Attempting 8 rapid-fire requests (1 every 0.1s)...")
    for i in range(1, 9):
        simulate_request(manager, user_id, i)
        print_status(counter, f"Post-Req #{i}")
        time.sleep(0.1)

    print("\nSCENARIO 2: Window Decay & Recovery")
    print("Strategy: Waiting 5 seconds and checking if capacity partially recovers...")
    print("   [WAIT] Sleeping for 5.0s...")
    time.sleep(5.0)
    print_status(counter, "After 5s sleep")
    
    # Try 3 more requests
    print("Strategy: Attempting 3 more requests...")
    for i in range(9, 12):
        simulate_request(manager, user_id, i)
        print_status(counter, f"Post-Req #{i}")
        time.sleep(0.1)

    print("\nSCENARIO 3: Complete Reset")
    print("Strategy: Waiting 10 seconds for the window to completely roll over...")
    print("   [WAIT] Sleeping for 10.0s...")
    time.sleep(10.0)
    print_status(counter, "After 10s sleep")
    
    print("Strategy: Attempting a request on a clean window...")
    simulate_request(manager, user_id, 12)
    print_status(counter, "Post-Req #12")

    print("\n==================================================")
    print("STATUS: SIMULATION COMPLETE")
    print("==================================================")

if __name__ == "__main__":
    run_rate_limit_simulation()
