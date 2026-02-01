import sys
import os
import time

# Add parent directory to path for core logic access
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.lru_cache import LRUCache

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class MockDatabase:
    """Simulates a slow database with artificial latency."""
    def __init__(self):
        self.data = {
            101: "Neural-Transformer-v4",
            102: "GPT-Lite-Signature",
            103: "ResNet-Feature-Extractor",
            104: "BERT-Sentiment-Analyzer",
            105: "Stable-Diffusion-Weights"
        }

    def fetch(self, model_id):
        print(f"  [DB] Fetching Model {model_id} from disk...")
        time.sleep(1.5)  # Simulate slow I/O
        return self.data.get(model_id, "Unknown Model")

def run_cache_simulation():
    clear_screen()
    print("--------------------------------------------------")
    print("SYSTEM: DATABASE QUERY ACCELERATOR")
    print("ALGORITHM: LRU CACHE (CAPACITY: 3)")
    print("--------------------------------------------------\n")

    db = MockDatabase()
    # Cache capacity is smaller than the DB size to force eviction logic
    cache = LRUCache(capacity=3)
    
    # Sequence of IDs to fetch (simulating user traffic)
    # Note: 101 and 102 are requested multiple times
    request_queue = [101, 102, 103, 101, 104, 102, 105]
    
    hits = 0
    misses = 0

    for i, model_id in enumerate(request_queue, 1):
        print(f"Request {i}: User wants Model {model_id}")
        
        # 1. Try to get from Cache
        result = cache.get(model_id)
        
        if result != -1:
            print(f"  [CACHE] HIT! Found '{result}' instantly.")
            hits += 1
        else:
            print(f"  [CACHE] MISS! Redirecting to Database...")
            misses += 1
            # 2. Fetch from DB
            result = db.fetch(model_id)
            # 3. Store in Cache for next time
            cache.put(model_id, result)
            print(f"  [CACHE] Saved '{result}' and updated LRU order.")

        print("-" * 40)

    # Final Report
    total = len(request_queue)
    print("\n--------------------------------------------------")
    print("ACCELERATION REPORT")
    print("--------------------------------------------------")
    print(f"Total Requests: {total}")
    print(f"Cache Hits:     {hits} (Instant)")
    print(f"Cache Misses:   {misses} (Slow DB Fetch)")
    print(f"Hit Rate:       {(hits/total)*100:.1f}%")
    print(f"Estimated Time Saved: ~{hits * 1.5} seconds")
    print("--------------------------------------------------")

if __name__ == "__main__":
    run_cache_simulation()