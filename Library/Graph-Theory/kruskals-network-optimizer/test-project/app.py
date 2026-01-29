import sys
import os
import json

# Add parent directory to path for core logic access
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.kruskal import KruskalMST

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_network_data(filepath):
    """Loads node names and potential edges from JSON."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None

def run_network_optimization():
    clear_screen()
    print("--------------------------------------------------")
    print("SYSTEM: REGIONAL NETWORK COST OPTIMIZER")
    print("ALGORITHM: KRUSKAL'S MINIMUM SPANNING TREE")
    print("--------------------------------------------------\n")

    data = load_network_data('locations.json')
    if not data:
        return

    nodes = data['nodes']
    # Format edges for the core logic: (cost, u, v)
    edges = [(c['cost'], c['u'], c['v']) for c in data['potential_connections']]

    print(f"Analyzing {len(nodes)} global data center nodes...")
    print(f"Evaluating {len(edges)} potential fiber-optic routes...\n")

    # Execute Kruskal's Algorithm
    mst_edges, min_total_cost = KruskalMST.calculate_mst(len(nodes), edges)

    # Output Professional Report
    print("OPTIMAL NETWORK TOPOLOGY IDENTIFIED:")
    print("--------------------------------------------------")
    for u, v, cost in mst_edges:
        print(f"  {nodes[u]} <---> {nodes[v]} | Cost: ${cost}M")

    print("--------------------------------------------------")
    print(f"TOTAL INFRASTRUCTURE INVESTMENT: ${min_total_cost}M")
    print("--------------------------------------------------")
    print("STATUS: Every node is now connected with zero cycles.")
    print("--------------------------------------------------")

if __name__ == "__main__":
    run_network_optimization()