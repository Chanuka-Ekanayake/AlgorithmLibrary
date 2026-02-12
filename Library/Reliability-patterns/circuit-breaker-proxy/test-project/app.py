import sys
import time
import random
from pathlib import Path

# Add parent directory to path for core logic access
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

try:
    from core.circuit_breaker import CircuitBreaker, State
except ImportError:
    print("❌ Error: Ensure 'core/circuit_breaker.py' and 'core/__init__.py' exist.")
    sys.exit(1)

# --- SIMULATED FLAKY SERVICE ---
def flaky_ml_inference_api(should_fail=False):
    """Simulates an external ML model server."""
    if should_fail:
        raise Exception("503 Service Unavailable: ML Model Server Overloaded")
    return {"status": "success", "prediction": random.uniform(0, 1)}

def run_stability_sim():
    print("--------------------------------------------------")
    print("SYSTEM: STABILITY SIMULATOR")
    print("ALGORITHM: CIRCUIT BREAKER PATTERN")
    print("--------------------------------------------------\n")

    # Initialize breaker: Trip after 3 failures, wait 5 seconds to retry
    breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=5.0)

    print("[PHASE 1] System Healthy. Processing requests...")
    for i in range(1, 4):
        res = breaker.call(flaky_ml_inference_api, should_fail=False)
        print(f"Request {i}: {res['status']} | {breaker.current_status}")
        time.sleep(0.5)

    print("\n[PHASE 2] Service Instability Detected! Injecting failures...")
    for i in range(1, 5):
        try:
            breaker.call(flaky_ml_inference_api, should_fail=True)
        except Exception as e:
            print(f"Request {i}: {e}")
        
        # Check if the breaker tripped
        if breaker.state == State.OPEN:
            print(f"--- NOTICE: {breaker.current_status} ---")
        time.sleep(0.5)

    print("\n[PHASE 3] Circuit is OPEN. Requests are failing fast (zero latency)...")
    for i in range(1, 4):
        try:
            breaker.call(flaky_ml_inference_api, should_fail=False)
        except Exception as e:
            print(f"Request {i}: {e}")
        time.sleep(0.5)

    print(f"\n[PHASE 4] Waiting {breaker.recovery_timeout}s for recovery timeout...")
    time.sleep(breaker.recovery_timeout + 0.1)

    print("\n[PHASE 5] Testing recovery (HALF-OPEN)...")
    try:
        # This call will move state to HALF-OPEN, and if successful, to CLOSED
        res = breaker.call(flaky_ml_inference_api, should_fail=False)
        print(f"Trial Request: {res['status']} | {breaker.current_status}")
    except Exception as e:
        print(f"Trial failed: {e}")

    print("\n[PHASE 6] Final Audit: Cluster back to normal.")
    res = breaker.call(flaky_ml_inference_api, should_fail=False)
    print(f"Final Request: {res['status']} | {breaker.current_status}")

    print("\n--------------------------------------------------")
    print("STATUS: SIMULATION COMPLETE")
    print("--------------------------------------------------")

if __name__ == "__main__":
    run_stability_sim()