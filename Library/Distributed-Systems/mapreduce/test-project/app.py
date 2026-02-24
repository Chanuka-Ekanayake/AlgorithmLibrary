import sys
import time
import random
from pathlib import Path

# Add parent directory for core logic
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

try:
    from core.mapreduce import MapReduceEngine
except ImportError:
    print("Error: Ensure 'core/mapreduce.py' and 'core/__init__.py' exist.")
    sys.exit(1)

# ==========================================
# SIMULATED DATA GENERATION
# ==========================================
def generate_logs(num_logs: int = 20000) -> list[str]:
    """Generates simulated Apache/Nginx server logs."""
    endpoints = [
        "/api/v1/products",
        "/api/v1/auth/login",
        "/api/v1/cart/checkout",
        "/health",
        "/images/logo.png"
    ]
    status_codes = [200, 201, 404, 500]
    
    logs = []
    print(f"[DATA] Generating {num_logs} simulated server logs...")
    for _ in range(num_logs):
        ip = f"192.168.1.{random.randint(1, 255)}"
        endpoint = random.choice(endpoints)
        status = random.choice(status_codes)
        # Log Format: "IP - - [Date] "GET /endpoint HTTP/1.1" Status"
        log_entry = f'{ip} - - [24/Feb/2026] "GET {endpoint} HTTP/1.1" {status}'
        logs.append(log_entry)
    
    return logs

# ==========================================
# MAPPER & REDUCER FUNCTIONS (Must be top-level)
# ==========================================
def log_mapper(log_line: str) -> list[tuple[str, int]]:
    """
    MAP STEP: Parses a raw log line and extracts the endpoint.
    Input: '192.168.1.5 ... "GET /api/v1/products ..."'
    Output: [("/api/v1/products", 1)]
    """
    try:
        # Simple string parsing to extract the URL
        parts = log_line.split('"')
        request_line = parts[1]  # "GET /api/v1/products HTTP/1.1"
        endpoint = request_line.split()[1]
        return [(endpoint, 1)]
    except IndexError:
        return []

def count_reducer(key: str, values: list[int]) -> tuple[str, int]:
    """
    REDUCE STEP: Sums the counts for a specific key.
    Input: "/api/v1/products", [1, 1, 1, 1...]
    Output: ("/api/v1/products", 4500)
    """
    return (key, sum(values))

# ==========================================
# MAIN EXECUTION
# ==========================================
def run_log_analyzer():
    print("-" * 65)
    print("SYSTEM: E-COMMERCE LOG ANALYZER")
    print("FRAMEWORK: MAPREDUCE (Multi-Process)")
    print("-" * 65 + "\n")

    # 1. Prepare Data
    raw_logs = generate_logs(20000)
    
    print("\n[PROCESSING] Distributing job across 4 CPU cores...")
    
    start_time = time.perf_counter()

    # 2. Execute MapReduce Job
    # We use 4 workers to simulate a 4-node cluster
    results = MapReduceEngine.execute(
        data=raw_logs,
        mapper=log_mapper,
        reducer=count_reducer,
        num_workers=4
    )
    
    end_time = time.perf_counter()

    # 3. Output Results
    print("\n" + "="*65)
    print("TRAFFIC REPORT")
    print("="*65)
    
    # Sort results by count (highest traffic first)
    sorted_stats = sorted(results.items(), key=lambda item: item[1][1], reverse=True)
    
    print(f"{'ENDPOINT':<30} | {'HITS':<10}")
    print("-" * 45)
    for endpoint, count_tuple in sorted_stats:
        # count_tuple is (endpoint, total_count) from reducer
        print(f"{endpoint:<30} | {count_tuple[1]:<10}")

    print("-" * 65)
    print(f"Total Logs Processed: {len(raw_logs)}")
    print(f"Execution Time:       {(end_time - start_time) * 1000:.4f} ms")
    print("="*65)
    print("RESULT: Distributed log analysis complete.")

if __name__ == "__main__":
    # Windows/macOS multiprocessing requires this guard
    run_log_analyzer()