import sys
import time
from pathlib import Path

# Add parent directory to path for core logic access
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

from core.bplus_tree import BPlusTree

def run_database_simulation():
    print("==================================================")
    print("DATABASE ENGINE: ToyDB Indexing Simulator")
    print("ALGORITHM: B+ Tree Indexing (Order M=4)")
    print("==================================================\n")

    # Initialize B+ Tree of order 4 (max 3 keys per node, 4 children)
    print("[INIT] Initializing Index Tree (Order = 4)...")
    db_index = BPlusTree(order=4)
    
    # Mock data to insert (User Records: ID -> Profile Details)
    users = [
        (15, {"name": "Alice", "role": "Admin"}),
        (8,  {"name": "Bob", "role": "User"}),
        (25, {"name": "Charlie", "role": "Manager"}),
        (5,  {"name": "David", "role": "User"}),
        (12, {"name": "Eve", "role": "Developer"}),
        (20, {"name": "Frank", "role": "QA"}),
        (30, {"name": "Grace", "role": "Designer"}),
        (35, {"name": "Heidi", "role": "Support"}),
    ]

    print("\n[INSERTION] Bulk inserting user profiles into database...")
    for uid, profile in users:
        print(f"   Inserting User ID {uid:2} -> {profile['name']}")
        db_index.insert(uid, profile)

    print("\n[TREE STRUCTURE] Visualizing resulting B+ Tree hierarchy:")
    print("--------------------------------------------------")
    print(db_index.visualize())
    print("--------------------------------------------------")

    print("\n[POINT QUERY] Looking up specific users...")
    lookups = [12, 30, 99]  # Existing and non-existing keys
    
    for key in lookups:
        # Simulate tree search
        result, tree_reads = db_index.search(key)
        
        # Simulate standard linear scan database cost
        if key in [u[0] for u in users]:
            linear_reads = [u[0] for u in users].index(key) + 1
        else:
            linear_reads = len(users)

        print(f"\n   Searching for User ID: {key}")
        if result:
            print(f"   -> Found: {result['name']} ({result['role']})")
        else:
            print(f"   -> Result: NOT FOUND")
        print(f"   Performance Comparison:")
        print(f"      - B+ Tree Index Reads : {tree_reads} pages")
        print(f"      - Linear Scan Reads   : {linear_reads} pages")

    print("\n[RANGE QUERY] Performing range scan query (ID between 10 and 28)...")
    start_id, end_id = 10, 28
    
    results, range_tree_reads = db_index.search_range(start_id, end_id)
    
    # Linear scan range query always has to scan the entire table
    linear_range_reads = len(users)

    print(f"   Retrieving users where {start_id} <= ID <= {end_id}:")
    for r_key, r_val in results:
        print(f"   -> ID {r_key:2}: {r_val['name']} ({r_val['role']})")
        
    print(f"   Performance Comparison:")
    print(f"      - B+ Tree Index Reads : {range_tree_reads} pages (Traverse to leaf + scan leaf list)")
    print(f"      - Linear Scan Reads   : {linear_range_reads} pages (Must check every single table row)")

    print("\n==================================================")
    print("STATUS: SIMULATION COMPLETE")
    print("==================================================")

if __name__ == "__main__":
    run_database_simulation()
