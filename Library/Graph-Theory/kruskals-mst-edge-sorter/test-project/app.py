"""
Kruskal's MST Edge Sorter - Interactive Demo

This application demonstrates Kruskal's Minimum Spanning Tree algorithm
using edge-based sorting and Union-Find for cycle detection.

Use Cases:
- Network design (minimize total cable/wire cost)
- Circuit board layout optimization
- Transportation network planning
- Clustering analysis

Author: Algorithm Library
"""

import sys
import os

# Add core module to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))

from kruskals_mst import (
    kruskals_mst,
    build_mst_graph,
    is_graph_connected,
    find_mst_forest,
    compare_edge_weights,
    get_critical_edges,
    calculate_mst_savings
)

def print_header():
    """Print application header."""
    print("=" * 70)
    print(" " * 20 + "KRUSKAL'S MST EDGE SORTER")
    print(" " * 18 + "Sort Edges, Unite Components")
    print("=" * 70)
    print()

def load_sample_network():
    """
    Load a sample telecommunications network.
    
    Scenario: Deploy fiber optic cables between 9 data centers.
    Edge weights represent cable installation costs in thousands.
    
    Returns:
        dict: Graph with data centers and costs
    """
    network = {
        'DC1': {'DC2': 4, 'DC8': 8},
        'DC2': {'DC1': 4, 'DC3': 8, 'DC8': 11},
        'DC3': {'DC2': 8, 'DC4': 7, 'DC6': 4, 'DC9': 2},
        'DC4': {'DC3': 7, 'DC5': 9, 'DC6': 14},
        'DC5': {'DC4': 9, 'DC6': 10},
        'DC6': {'DC3': 4, 'DC4': 14, 'DC5': 10, 'DC7': 2},
        'DC7': {'DC6': 2, 'DC8': 1, 'DC9': 6},
        'DC8': {'DC1': 8, 'DC2': 11, 'DC7': 1, 'DC9': 7},
        'DC9': {'DC3': 2, 'DC7': 6, 'DC8': 7}
    }
    
    return network

def load_custom_network():
    """
    Build custom network from user input.
    
    Returns:
        dict: User-defined graph
    """
    print("\n--- Custom Network Builder ---")
    print("Enter connections (format: NodeA NodeB cost)")
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
            print("❌ Invalid cost. Enter a number.")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return graph

def print_network_info(graph):
    """Display network statistics."""
    num_nodes = len(graph)
    num_edges = sum(len(neighbors) for neighbors in graph.values()) // 2
    
    total_cost = sum(
        weight for neighbors in graph.values()
        for weight in neighbors.values()
    ) / 2
    
    print("\n" + "─" * 70)
    print("📊 NETWORK INFORMATION")
    print("─" * 70)
    print(f"Data Centers:        {num_nodes}")
    print(f"Possible Connections: {num_edges}")
    print(f"Total Cost (all):    ${total_cost:.2f}K")
    
    if num_nodes > 1:
        density = (2 * num_edges) / (num_nodes * (num_nodes - 1)) * 100
        print(f"Network Density:     {density:.1f}%")
    
    print("─" * 70)

def visualize_sorted_edges(graph):
    """Display all edges sorted by weight."""
    edges = []
    seen = set()
    
    for u in graph:
        for v, weight in graph[u].items():
            edge_id = tuple(sorted([u, v]))
            if edge_id not in seen:
                edges.append((weight, u, v))
                seen.add(edge_id)
    
    edges.sort()
    
    print("\n📋 ALL EDGES (Sorted by Cost):")
    print("─" * 70)
    
    for i, (weight, u, v) in enumerate(edges, 1):
        print(f"{i:2}. {u:6} ━━ ${weight:6.2f}K ━━ {v}")
    
    print("─" * 70)

def visualize_mst_construction(graph):
    """Show step-by-step MST construction using Kruskal's."""
    from kruskals_mst import UnionFind
    
    # Extract and sort edges
    edges = []
    seen = set()
    
    for u in graph:
        for v, weight in graph[u].items():
            edge_id = tuple(sorted([u, v]))
            if edge_id not in seen:
                edges.append((weight, u, v))
                seen.add(edge_id)
    
    edges.sort()
    
    print("\n🔧 KRUSKAL'S ALGORITHM - STEP BY STEP")
    print("=" * 70)
    
    vertices = list(graph.keys())
    uf = UnionFind(vertices)
    
    mst_edges = []
    total_cost = 0
    step = 1
    
    print(f"\n📌 Initial: {len(vertices)} separate components")
    print(f"   Components: {', '.join(['{' + v + '}' for v in vertices[:5]])}{'...' if len(vertices) > 5 else ''}")
    
    for weight, u, v in edges:
        print(f"\n--- Step {step}: Consider edge {u} ━━ {v} (${weight}K) ---")
        
        root_u = uf.find(u)
        root_v = uf.find(v)
        
        if root_u == root_v:
            print(f"   ❌ Skip: {u} and {v} already in same component")
            print(f"      (would create cycle)")
        else:
            print(f"   ✅ Add to MST!")
            print(f"      {u} component: {root_u}")
            print(f"      {v} component: {root_v}")
            print(f"      → Unite components")
            
            uf.union(u, v)
            mst_edges.append((u, v, weight))
            total_cost += weight
            
            print(f"      MST edges so far: {len(mst_edges)}")
            print(f"      Total cost: ${total_cost:.2f}K")
            
            if len(mst_edges) == len(vertices) - 1:
                print(f"\n🎉 MST COMPLETE! All {len(vertices)} nodes connected.")
                break
        
        step += 1
        
        if step > 15:  # Limit output for large graphs
            print("\n   (... remaining steps omitted for brevity ...)")
            break
    
    print("\n" + "=" * 70)
    return mst_edges, total_cost

def display_mst_results(graph, mst_edges, total_cost):
    """Display comprehensive MST analysis."""
    print("\n" + "═" * 70)
    print(" " * 25 + "MST RESULTS")
    print("═" * 70)
    
    print(f"\n✅ Minimum Spanning Tree Found!")
    print(f"   Total Cost: ${total_cost:.2f}K")
    print(f"   Edges Used: {len(mst_edges)} of {sum(len(n) for n in graph.values()) // 2}")
    
    # Savings
    savings = calculate_mst_savings(graph, total_cost)
    if savings > 0:
        full_cost = sum(w for n in graph.values() for w in n.values()) / 2
        savings_percent = (savings / full_cost) * 100
        print(f"   💰 Savings: ${savings:.2f}K ({savings_percent:.1f}%)")
    
    # Edge statistics
    stats = compare_edge_weights(mst_edges)
    print(f"\n📊 EDGE STATISTICS:")
    print(f"   Cheapest Edge: ${stats['min_weight']:.2f}K")
    print(f"   Most Expensive: ${stats['max_weight']:.2f}K")
    print(f"   Average Cost: ${stats['avg_weight']:.2f}K")
    print(f"   Cost Range: ${stats['weight_range']:.2f}K")
    
    # MST edges
    print(f"\n🌳 MST EDGES (by weight):")
    print("─" * 70)
    
    for u, v, weight in sorted(mst_edges, key=lambda x: x[2]):
        print(f"   {u:8} ━━━ ${weight:6.2f}K ━━━ {v}")
    
    print("═" * 70)

def analyze_critical_edges(graph, mst_edges):
    """Identify most critical connections."""
    print("\n🔍 CRITICAL EDGE ANALYSIS:")
    print("─" * 70)
    print("⚠️  All MST edges are critical!")
    print("   Removing ANY edge disconnects the network.\n")
    
    critical = get_critical_edges(graph, mst_edges)
    
    print("💸 Most Expensive Critical Edges (highest impact):")
    for i, (u, v, cost) in enumerate(critical[:5], 1):
        print(f"   {i}. {u} ↔ {v}: ${cost:.2f}K")
    
    print("\n💎 Most Cost-Effective Critical Edges:")
    for i, (u, v, cost) in enumerate(sorted(mst_edges, key=lambda x: x[2])[:5], 1):
        print(f"   {i}. {u} ↔ {v}: ${cost:.2f}K")
    
    print("─" * 70)

def compare_with_prims():
    """Show comparison between Kruskal's and Prim's."""
    print("\n📚 ALGORITHM COMPARISON")
    print("─" * 70)
    print("Kruskal's vs Prim's MST:\n")
    print("Aspect           | Kruskal's          | Prim's")
    print("-----------------|--------------------|-----------------")
    print("Approach         | Global edge sort   | Local growth")
    print("Data Structure   | Union-Find         | Priority Queue")
    print("Time Complexity  | O(E log E)         | O(E log V)")
    print("Best For         | Sparse graphs      | Dense graphs")
    print("Starting Vertex  | Not needed         | Required")
    print("Disconnected     | Handles naturally  | Needs modification")
    print("\nOur Implementation: Edge-based with optimized Union-Find")
    print("─" * 70)

def handle_disconnected_graph(graph):
    """Find MST forest for disconnected graph."""
    print("\n🌲 HANDLING DISCONNECTED GRAPH")
    print("─" * 70)
    
    forest = find_mst_forest(graph)
    
    if len(forest) == 1:
        print("Graph is connected! Single MST found.")
        return forest[0]
    
    print(f"Graph has {len(forest)} disconnected components.")
    print("Finding MST for each component (Minimum Spanning Forest):\n")
    
    total_forest_cost = 0
    
    for i, (mst_edges, cost) in enumerate(forest, 1):
        total_forest_cost += cost
        print(f"Component {i}:")
        print(f"  Edges: {len(mst_edges)}")
        print(f"  Cost: ${cost:.2f}K")
        print(f"  Nodes: {len(set([u for u,v,w in mst_edges] + [v for u,v,w in mst_edges]))}")
    
    print(f"\nTotal Forest Cost: ${total_forest_cost:.2f}K")
    print("─" * 70)
    
    return None

def main_menu():
    """Display main menu and handle user choices."""
    graph = None
    mst_edges = None
    total_cost = None
    
    while True:
        print("\n" + "═" * 70)
        print("MAIN MENU")
        print("═" * 70)
        print("1. Load Sample Network (9 data centers)")
        print("2. Build Custom Network")
        print("3. Display Network Info")
        print("4. Show All Edges (Sorted)")
        print("5. Calculate MST (Step-by-Step)")
        print("6. Calculate MST (Direct)")
        print("7. Analyze Critical Edges")
        print("8. Compare Algorithms (Kruskal's vs Prim's)")
        print("9. Exit")
        print("═" * 70)
        
        choice = input("\nSelect option (1-9): ").strip()
        
        if choice == '1':
            graph = load_sample_network()
            mst_edges = None
            total_cost = None
            print("✅ Sample network loaded!")
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
                
        elif choice == '4':
            if not graph:
                print("❌ No network loaded.")
            else:
                visualize_sorted_edges(graph)
                
        elif choice == '5':
            if not graph:
                print("❌ No network loaded.")
            else:
                if not is_graph_connected(graph):
                    print("⚠️  Graph is disconnected!")
                    handle_disconnected_graph(graph)
                    continue
                
                result = visualize_mst_construction(graph)
                if result:
                    mst_edges, total_cost = result
                    
        elif choice == '6':
            if not graph:
                print("❌ No network loaded.")
            else:
                if not is_graph_connected(graph):
                    print("⚠️  Graph is disconnected!")
                    handle_disconnected_graph(graph)
                    continue
                
                print("\n🔧 Calculating MST using Kruskal's algorithm...")
                result = kruskals_mst(graph)
                
                if result:
                    mst_edges, total_cost = result
                    display_mst_results(graph, mst_edges, total_cost)
                else:
                    print("❌ Failed to calculate MST.")
                    
        elif choice == '7':
            if not mst_edges:
                print("❌ Calculate MST first (option 5 or 6).")
            else:
                analyze_critical_edges(graph, mst_edges)
                
        elif choice == '8':
            compare_with_prims()
            
        elif choice == '9':
            print("\n" + "═" * 70)
            print("Thank you for using Kruskal's MST Edge Sorter!")
            print("═" * 70)
            break
            
        else:
            print("❌ Invalid option. Choose 1-9.")

def main():
    """Main application entry point."""
    print_header()
    
    print("Welcome to Kruskal's MST Edge Sorter!")
    print()
    print("This tool demonstrates Kruskal's algorithm:")
    print("  1. Sort all edges by weight")
    print("  2. Add edges in order (skip if creates cycle)")
    print("  3. Use Union-Find for efficient cycle detection")
    print()
    print("Perfect for:")
    print("  • Network design with global cost optimization")
    print("  • Understanding edge-based MST construction")
    print("  • Learning Union-Find data structure")
    print()
    input("Press Enter to continue...")
    
    main_menu()

if __name__ == "__main__":
    main()
