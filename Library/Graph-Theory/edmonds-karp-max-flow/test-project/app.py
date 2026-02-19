import sys
import os

# Add the parent directory to sys.path to import the core module
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from core.edmonds_karp import get_max_flow

def main():
    print("--------------------------------------------------------")
    print("     Edmonds-Karp Max Flow Algorithm Demonstration      ")
    print("--------------------------------------------------------")
    print("Scenario: Network Data Packet Optimization")
    print("Goal: Calculate the maximum data throughput from Server A to Server Z.")
    print("--------------------------------------------------------\n")

    # Define a sample flow network
    # Graph structure: { 'Node': { 'Neighbor': Capacity } }
    network = {
        'A': {'B': 1000, 'C': 1000},
        'B': {'C': 1, 'D': 1000},
        'C': {'D': 1000},
        'D': {'Z': 2000},
        'Z': {}
    }

    source_node = 'A'
    sink_node = 'Z'

    print(f"Network Topology:")
    for node, neighbors in network.items():
        for neighbor, capacity in neighbors.items():
            print(f"  {node} -> {neighbor} [Capacity: {capacity} Mbps]")
    
    print(f"\nSource: {source_node}")
    print(f"Sink:   {sink_node}")
    print("\nCalculating Max Flow...")

    max_flow, residual_graph = get_max_flow(network, source_node, sink_node)

    print(f"\n>>> Maximum Throughput: {max_flow} Mbps")
    print("--------------------------------------------------------")

    # Verification Step for the User
    expected_flow = 2000
    if max_flow == expected_flow:
        print("\n[SUCCESS] The algorithm calculated the correct max flow.")
    else:
        print(f"\n[FAILURE] Expected {expected_flow}, but got {max_flow}.")

if __name__ == "__main__":
    main()
