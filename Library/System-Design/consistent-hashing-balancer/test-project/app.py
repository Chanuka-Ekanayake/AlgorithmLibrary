import sys
from pathlib import Path
from collections import Counter

# Add parent directory to path for core logic access
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

try:
    from core.hash_ring import ConsistentHashRing
except ImportError:
    print("Error: Ensure 'core/hash_ring.py' and 'core/__init__.py' exist.")
    sys.exit(1)

def run_balancer_simulation():
    print("--------------------------------------------------")
    print("SYSTEM: GLOBAL LOAD BALANCER")
    print("ALGORITHM: CONSISTENT HASHING (VIRTUAL NODES)")
    print("--------------------------------------------------\n")

    # 1. Initialize the cluster with 3 servers
    initial_nodes = ["Server-Alpha", "Server-Beta", "Server-Gamma"]
    # We use 100 virtual nodes per physical node for smooth distribution
    ring = ConsistentHashRing(nodes=initial_nodes, virtual_nodes=100)
    
    print(f"[CLUSTER] Initialized with: {', '.join(initial_nodes)}")
    print(f"[INFO] Total virtual points on ring: {len(ring.sorted_keys)}\n")

    # 2. Simulate 10,000 requests for software/ML models
    requests = [f"download_request_{i}" for i in range(10000)]
    
    def get_stats(ring_obj, req_list):
        counts = Counter()
        for req in req_list:
            node = ring_obj.get_node(req)
            counts[node] += 1
        return counts

    print("SCENARIO 1: Initial Traffic Distribution")
    stats1 = get_stats(ring, requests)
    for node, count in stats1.items():
        print(f"  {node}: {count} requests ({(count/10000)*100:.2f}%)")

    # 3. Scale Up: Adding a new server
    print("\nSCENARIO 2: Scaling Up (Adding Server-Delta)")
    ring.add_node("Server-Delta")
    
    # Calculate how many keys actually moved
    moved_keys = 0
    for req in requests:
    for req in requests:
        if ring.get_node(req) == "Server-Delta":
            moved_keys += 1
            
    print(f"  Result: Server-Delta captured {moved_keys} requests.")
    print(f"  Efficiency: Only {(moved_keys/10000)*100:.2f}% of data was re-mapped.")
    print("  (Standard hashing would have re-mapped ~75%+ of data)")

    # 4. Fault Tolerance: Server-Beta Crashes
    print("\nSCENARIO 3: Fault Tolerance (Server-Beta Offline)")
    ring.remove_node("Server-Beta")
    stats3 = get_stats(ring, requests)
    
    print("  New Distribution:")
    for node, count in sorted(stats3.items()):
        print(f"  {node}: {count} requests")

    print("\n--------------------------------------------------")
    print("STATUS: LOAD BALANCING SUCCESSFUL")
    print("Consistent Hashing maintained cluster stability.")
    print("--------------------------------------------------")

if __name__ == "__main__":
    run_balancer_simulation()