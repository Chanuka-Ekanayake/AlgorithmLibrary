"""
Prim's MST Network Infrastructure Optimizer - Interactive Demo

This application demonstrates Prim's Minimum Spanning Tree algorithm
for optimizing network infrastructure deployment costs.

Use Cases:
- Cable network installation (fiber optic, power, telecom)
- Road/highway network planning
- Pipeline network design
- Circuit board trace optimization

Author: Algorithm Library
"""

import sys
import os

# Add core module to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))

from prims_mst import (
    prims_mst,
    build_mst_graph,
    is_graph_connected,
    calculate_mst_savings,
    get_mst_diameter,
    get_mst_statistics
)

def print_header():
    """Print application header."""
    print("=" * 70)
    print(" " * 15 + "NETWORK INFRASTRUCTURE OPTIMIZER")
    print(" " * 20 + "Using Prim's MST Algorithm")
    print("=" * 70)
    print()

def load_sample_network():
    """
    Load a sample city network infrastructure.
    
    Scenario: Deploy fiber optic cables to connect 9 city districts.
    Edge weights represent installation costs in thousands of dollars.
    
    Returns:
        dict: Graph with districts and cable costs
    """
    # City districts network
    network = {
        'Downtown': {'Midtown': 15, 'Industrial': 25, 'Harbor': 30},
        'Midtown': {'Downtown': 15, 'University': 12, 'Shopping': 18},
        'University': {'Midtown': 12, 'Shopping': 10, 'Residential': 20},
        'Shopping': {'Midtown': 18, 'University': 10, 'Suburban': 14, 'Harbor': 22},
        'Residential': {'University': 20, 'Suburban': 8, 'Airport': 35},
        'Suburban': {'Shopping': 14, 'Residential': 8, 'Airport': 16},
        'Industrial': {'Downtown': 25, 'Harbor': 20},
        'Harbor': {'Downtown': 30, 'Shopping': 22, 'Industrial': 20, 'Airport': 28},
        'Airport': {'Residential': 35, 'Suburban': 16, 'Harbor': 28}
    }
    
    return network

def load_custom_network():
    """
    Load a custom network from user input or file.
    
    Returns:
        dict: User-defined graph
    """
    print("\n--- Custom Network Builder ---")
    print("Enter network connections (format: NodeA NodeB cost)")
    print("Type 'done' when finished")
    print()
    
    graph = {}
    
    while True:
        line = input("Connection: ").strip()
        
        if line.lower() == 'done':
            break
        
        try:
            parts = line.split()
            if len(parts) != 3:
                print("❌ Invalid format. Use: NodeA NodeB cost")
                continue
            
            node_a, node_b, cost = parts[0], parts[1], float(parts[2])
            
            # Add bidirectional edge
            if node_a not in graph:
                graph[node_a] = {}
            if node_b not in graph:
                graph[node_b] = {}
            
            graph[node_a][node_b] = cost
            graph[node_b][node_a] = cost
            
            print(f"✅ Added: {node_a} ↔ {node_b} (${cost}K)")
            
        except ValueError:
            print("❌ Invalid cost value. Please enter a number.")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return graph

def print_network_info(graph):
    """
    Display network statistics.
    
    Args:
        graph: Network graph
    """
    num_nodes = len(graph)
    num_edges = sum(len(neighbors) for neighbors in graph.values()) // 2
    
    total_cost = sum(
        weight for neighbors in graph.values()
        for weight in neighbors.values()
    ) / 2  # Divide by 2 since edges counted twice
    
    print("\n" + "─" * 70)
    print("📊 NETWORK INFORMATION")
    print("─" * 70)
    print(f"Districts/Nodes:     {num_nodes}")
    print(f"Possible Connections: {num_edges}")
    print(f"Total Infrastructure Cost (all connections): ${total_cost:.2f}K")
    
    if num_nodes > 0:
        density = (2 * num_edges) / (num_nodes * (num_nodes - 1)) * 100 if num_nodes > 1 else 0
        print(f"Network Density:     {density:.1f}%")
    
    print("─" * 70)

def visualize_graph(graph, title="Network Graph"):
    """
    Display ASCII visualization of the graph.
    
    Args:
        graph: Network graph
        title: Display title
    """
    print(f"\n{title}:")
    print("─" * 70)
    
    for node in sorted(graph.keys()):
        neighbors = graph[node]
        if neighbors:
            connections = [f"{neighbor}(${cost}K)" for neighbor, cost in sorted(neighbors.items())]
            print(f"{node:15} → {', '.join(connections)}")
        else:
            print(f"{node:15} → (isolated)")
    
    print("─" * 70)

def visualize_mst(mst_edges):
    """
    Display MST in ASCII tree format.
    
    Args:
        mst_edges: List of (from, to, weight) tuples
    """
    print("\n🌳 MST STRUCTURE (Tree View):")
    print("─" * 70)
    
    if not mst_edges:
        print("(Empty MST)")
        return
    
    # Build adjacency list from MST edges
    mst_adj = {}
    all_nodes = set()
    
    for u, v, weight in mst_edges:
        if u not in mst_adj:
            mst_adj[u] = []
        if v not in mst_adj:
            mst_adj[v] = []
        
        mst_adj[u].append((v, weight))
        mst_adj[v].append((u, weight))
        all_nodes.add(u)
        all_nodes.add(v)
    
    # Print edges sorted
    for u, v, weight in sorted(mst_edges, key=lambda x: x[2]):
        print(f"  {u:15} ━━━━ ${weight:6.2f}K ━━━━ {v}")
    
    print("─" * 70)

def display_mst_results(graph, mst_edges, total_cost):
    """
    Display comprehensive MST analysis results.
    
    Args:
        graph: Original graph
        mst_edges: MST edges
        total_cost: MST total cost
    """
    print("\n" + "═" * 70)
    print(" " * 25 + "MST OPTIMIZATION RESULTS")
    print("═" * 70)
    
    # Basic info
    print(f"\n✅ Minimum Spanning Tree Found!")
    print(f"   Total Cost: ${total_cost:.2f}K")
    print(f"   Edges Used: {len(mst_edges)} of {sum(len(n) for n in graph.values()) // 2} possible")
    
    # Savings
    savings = calculate_mst_savings(graph, total_cost)
    if savings > 0:
        full_cost = sum(w for n in graph.values() for w in n.values()) / 2
        savings_percent = (savings / full_cost) * 100
        print(f"   💰 Cost Savings: ${savings:.2f}K ({savings_percent:.1f}%)")
    
    # Build MST graph for further analysis
    mst_graph = build_mst_graph(mst_edges)
    
    # Diameter
    diameter = get_mst_diameter(mst_graph)
    print(f"   📏 Network Diameter: ${diameter:.2f}K (longest path)")
    
    # Statistics
    stats = get_mst_statistics(mst_graph)
    print(f"\n📈 NETWORK STATISTICS:")
    print(f"   Average Node Degree: {stats['avg_degree']:.2f}")
    print(f"   Max Node Degree (hub): {stats['max_degree']} ({stats['max_degree_node']})")
    print(f"   Leaf Nodes: {stats['leaf_count']}")
    
    if stats['leaf_nodes']:
        print(f"   Leaf Districts: {', '.join(sorted(stats['leaf_nodes']))}")
    
    print("═" * 70)

def analyze_critical_connections(mst_edges):
    """
    Identify critical network connections.
    
    Args:
        mst_edges: MST edges
    """
    print("\n🔍 CRITICAL CONNECTION ANALYSIS:")
    print("─" * 70)
    
    # All edges are critical in an MST (removing any disconnects network)
    print("⚠️  All MST edges are CRITICAL - removing any edge disconnects the network!")
    print()
    
    # Find most expensive (highest impact) connections
    sorted_edges = sorted(mst_edges, key=lambda x: x[2], reverse=True)
    
    print("💸 Top 5 Most Expensive Connections:")
    for i, (u, v, cost) in enumerate(sorted_edges[:5], 1):
        print(f"   {i}. {u} ↔ {v}: ${cost:.2f}K")
    
    print("\n💎 Top 5 Most Cost-Effective Connections:")
    sorted_edges_cheap = sorted(mst_edges, key=lambda x: x[2])
    for i, (u, v, cost) in enumerate(sorted_edges_cheap[:5], 1):
        print(f"   {i}. {u} ↔ {v}: ${cost:.2f}K")
    
    print("─" * 70)

def simulate_network_expansion(graph, mst_edges):
    """
    Simulate adding a new district to the network.
    
    Args:
        graph: Original graph
        mst_edges: Current MST
    """
    print("\n🏗️  NETWORK EXPANSION SIMULATOR")
    print("─" * 70)
    
    existing_nodes = set(graph.keys())
    
    new_district = input("Enter new district name: ").strip()
    
    if not new_district or new_district in existing_nodes:
        print("❌ Invalid or duplicate district name.")
        return
    
    print(f"\nConnecting '{new_district}' to existing districts:")
    print("Enter connection costs (format: ExistingDistrict cost)")
    print("Type 'done' when finished")
    
    connections = {}
    
    while True:
        line = input(f"{new_district} → ").strip()
        
        if line.lower() == 'done':
            break
        
        try:
            parts = line.split()
            if len(parts) != 2:
                print("❌ Use format: ExistingDistrict cost")
                continue
            
            target, cost = parts[0], float(parts[1])
            
            if target not in existing_nodes:
                print(f"❌ '{target}' not in existing network.")
                continue
            
            connections[target] = cost
            print(f"✅ Added potential connection to {target}: ${cost}K")
            
        except ValueError:
            print("❌ Invalid cost value.")
    
    if not connections:
        print("❌ No connections specified.")
        return
    
    # Find minimum cost connection
    min_connection = min(connections.items(), key=lambda x: x[1])
    best_target, best_cost = min_connection
    
    print(f"\n📊 EXPANSION ANALYSIS:")
    print(f"   Best Connection: {new_district} ↔ {best_target}")
    print(f"   Additional Cost: ${best_cost:.2f}K")
    
    current_mst_cost = sum(cost for _, _, cost in mst_edges)
    new_total = current_mst_cost + best_cost
    
    print(f"   New Total Network Cost: ${new_total:.2f}K")
    print(f"   Cost Increase: {(best_cost / current_mst_cost * 100):.1f}%")
    
    print("─" * 70)

def compare_algorithms_info():
    """Display comparison with other MST algorithms."""
    print("\n📚 ALGORITHM COMPARISON")
    print("─" * 70)
    print("Prim's vs Other MST Algorithms:")
    print()
    print("Algorithm      | Time          | Best For")
    print("---------------|---------------|--------------------------------")
    print("Prim's (Heap)  | O(E log V)    | Dense graphs, incremental")
    print("Kruskal's      | O(E log E)    | Sparse graphs, simple implementation")
    print("Borůvka's      | O(E log V)    | Parallel processing")
    print()
    print("Our Implementation: Prim's with Binary Heap (Priority Queue)")
    print("─" * 70)

def main_menu():
    """Display main menu and handle user choices."""
    graph = None
    mst_edges = None
    total_cost = None
    
    while True:
        print("\n" + "═" * 70)
        print("MAIN MENU")
        print("═" * 70)
        print("1. Load Sample City Network (9 districts)")
        print("2. Build Custom Network")
        print("3. Display Current Network")
        print("4. Calculate Minimum Spanning Tree (MST)")
        print("5. Analyze Critical Connections")
        print("6. Simulate Network Expansion")
        print("7. Algorithm Information")
        print("8. Exit")
        print("═" * 70)
        
        choice = input("\nSelect option (1-8): ").strip()
        
        if choice == '1':
            graph = load_sample_network()
            mst_edges = None
            total_cost = None
            print("✅ Sample city network loaded!")
            print_network_info(graph)
            
        elif choice == '2':
            graph = load_custom_network()
            mst_edges = None
            total_cost = None
            if graph:
                print("✅ Custom network created!")
                print_network_info(graph)
            else:
                print("❌ No network created.")
                
        elif choice == '3':
            if not graph:
                print("❌ No network loaded. Choose option 1 or 2 first.")
            else:
                print_network_info(graph)
                visualize_graph(graph, "Current Network")
                
        elif choice == '4':
            if not graph:
                print("❌ No network loaded. Choose option 1 or 2 first.")
            else:
                if not is_graph_connected(graph):
                    print("❌ Network is disconnected! MST requires connected graph.")
                    continue
                
                print("\n🔧 Calculating Minimum Spanning Tree...")
                
                # Let user choose starting node
                nodes = sorted(graph.keys())
                print(f"\nAvailable districts: {', '.join(nodes)}")
                start = input("Starting district (or press Enter for auto): ").strip()
                
                if start and start not in nodes:
                    print(f"❌ '{start}' not found. Using auto-selection.")
                    start = None
                
                # Calculate MST
                result = prims_mst(graph, start)
                
                if result is None:
                    print("❌ Failed to calculate MST.")
                else:
                    mst_edges, total_cost = result
                    display_mst_results(graph, mst_edges, total_cost)
                    visualize_mst(mst_edges)
                    
        elif choice == '5':
            if mst_edges is None:
                print("❌ Calculate MST first (option 4).")
            else:
                analyze_critical_connections(mst_edges)
                
        elif choice == '6':
            if mst_edges is None:
                print("❌ Calculate MST first (option 4).")
            else:
                simulate_network_expansion(graph, mst_edges)
                
        elif choice == '7':
            compare_algorithms_info()
            
        elif choice == '8':
            print("\n" + "═" * 70)
            print("Thank you for using Network Infrastructure Optimizer!")
            print("═" * 70)
            break
            
        else:
            print("❌ Invalid option. Please choose 1-8.")

def main():
    """Main application entry point."""
    print_header()
    
    print("Welcome to the Network Infrastructure Optimizer!")
    print()
    print("This tool uses Prim's Minimum Spanning Tree algorithm to find")
    print("the most cost-effective way to connect all locations in a network.")
    print()
    print("Perfect for planning:")
    print("  • Fiber optic cable networks")
    print("  • Power grid infrastructure")
    print("  • Road/highway systems")
    print("  • Pipeline networks")
    print()
    input("Press Enter to continue...")
    
    main_menu()

if __name__ == "__main__":
    main()
