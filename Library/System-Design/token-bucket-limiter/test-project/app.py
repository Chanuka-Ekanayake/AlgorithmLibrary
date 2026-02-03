import sys
import os
import time
from concurrent.futures import ThreadPoolExecutor

# Add parent directory to path for core logic access
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.rate_limiter import RateLimitManager

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def simulate_request(manager, user_id, request_num):
    """Simulates a single API call attempt."""
    allowed = manager.is_allowed(user_id)
    status = "✅ 200 OK" if allowed else "❌ 429 TOO MANY REQUESTS"
    print(f"[{user_id}] Request #{request_num:02d}: {status}")
    return allowed

def run_rate_limit_simulation():
    clear_screen()
    print("--------------------------------------------------")
    print("SYSTEM: API ENDPOINT SHIELD")
    print("ALGORITHM: TOKEN BUCKET (THREAD-SAFE)")
    print("--------------------------------------------------\n")

    # Tier 1: 'Free-User' (Low Capacity, Slow Refill)
    # 5 burst requests allowed, refills 1 per second
    free_manager = RateLimitManager(default_capacity=5, default_refill_rate=1.0)
    
    # Tier 2: 'Pro-User' (High Capacity, Fast Refill)
    # 50 burst requests allowed, refills 10 per second
    pro_manager = RateLimitManager(default_capacity=50, default_refill_rate=10.0)

    print("SCENARIO 1: The 'Free User' Spam Attack")
    print("Strategy: Attempting 10 rapid-fire requests...")
    for i in range(1, 11):
        simulate_request(free_manager, "Free-User-01", i)
        time.sleep(0.1) # Fast requests
    
    print("\n[WAIT] Waiting 2 seconds for bucket to refill...")
    time.sleep(2)
    
    print("\nSCENARIO 2: Post-Refill Recovery")
    for i in range(11, 14):
        simulate_request(free_manager, "Free-User-01", i)
    
    print("\n" + "="*50)
    print("SCENARIO 3: 'Pro User' High Throughput")
    print("Strategy: Handling a larger burst smoothly...")
    for i in range(1, 16):
        simulate_request(pro_manager, "Pro-Developer-Alpha", i)
        time.sleep(0.05)

    print("\n--------------------------------------------------")
    print("STATUS: INFRASTRUCTURE PROTECTED")
    print("All '429' errors successfully intercepted by the shield.")
    print("--------------------------------------------------")

if __name__ == "__main__":
    run_rate_limit_simulation()