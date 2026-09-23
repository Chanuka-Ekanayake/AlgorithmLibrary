"""
Borůvka's MST Global Network Optimizer — Interactive Demo

This application demonstrates Borůvka's Minimum Spanning Tree algorithm
for optimizing global data center network infrastructure costs.

The algorithm finds the cheapest way to connect all data center hubs
using its unique component-merging strategy, where each region
independently identifies its cheapest cross-region link.

Use Cases:
- Submarine cable network planning
- Global CDN backbone design
- Multi-region cloud infrastructure
- Distributed sensor network deployment

Author: Algorithm Library
"""

import sys
import os
import json

# Add core module to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))

from boruvka import (
    boruvkas_mst,
    is_graph_connected,
    calculate_mst_savings,
    get_mst_statistics,
)


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def load_network_data(filepath):
    """
    Loads data center nodes and potential cable routes from JSON.

    Args:
        filepath: Path to the JSON network data file.

    Returns:
        Parsed JSON data or None on error.
    """
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None


def build_graph_from_data(data):
    """
    Converts JSON network data into adjacency list format.

    Args:
        data: Parsed JSON with 'nodes' and 'potential_connections'.

    Returns:
        Graph as adjacency list {node: {neighbor: weight}}.
    """
    graph = {}
    for node in data['nodes']:
        graph[node] = {}

    for connection in data['potential_connections']:
        u, v, cost = connection['u'], connection['v'], connection['cost']
        graph[u][v] = cost
        graph[v][u] = cost

    return graph


def print_header():
    """Print application header."""
    print("=" * 70)
    print(" " * 10 + "GLOBAL DATA CENTER NETWORK OPTIMIZER")
    print(" " * 12 + "Using Boruvka's MST Algorithm")
    print("=" * 70)
    print()


def print_separator():
    """Print a visual separator line."""
    print("-" * 70)


def display_network_summary(data, graph):
    """
    Display a summary of the network being analyzed.

    Args:
        data: Parsed JSON data.
        graph: Graph adjacency list.
    """
    print("NETWORK ANALYSIS INPUT")
    print_separator()
    print(f"  Data Center Hubs:         {len(data['nodes'])}")
    print(f"  Potential Cable Routes:   {len(data['potential_connections'])}")
    print()

    print("  Hub Locations:")
    for i, node in enumerate(data['nodes'], 1):
        connections = len(graph[node])
        print(f"    {i}. {node:<20} ({connections} possible routes)")

    print()
    connected = is_graph_connected(graph)
    status = "[OK] CONNECTED" if connected else "[X] DISCONNECTED"
    print(f"  Network Connectivity:     {status}")
    print_separator()
    print()


def display_mst_result(mst_edges, total_cost):
    """
    Display the optimal MST result in a professional report format.

    Args:
        mst_edges: List of (u, v, weight) tuples forming the MST.
        total_cost: Total weight of the MST.
    """
    print("OPTIMAL NETWORK TOPOLOGY IDENTIFIED")
    print_separator()
    print()

    print("  Selected Cable Routes (Boruvka's MST):")
    print()
    for i, (u, v, cost) in enumerate(mst_edges, 1):
        print(f"    {i}. {u:<16} <===> {v:<16}  Cost: ${cost}M")

    print()
    print_separator()
    print(f"  TOTAL INFRASTRUCTURE INVESTMENT:  ${total_cost}M")
    print_separator()
    print()


def display_savings_analysis(graph, mst_edges):
    """
    Display cost savings analysis comparing MST vs full network.

    Args:
        graph: Original graph.
        mst_edges: MST edges.
    """
    total_cost, mst_cost, savings_pct = calculate_mst_savings(graph, mst_edges)

    print("COST SAVINGS ANALYSIS")
    print_separator()
    print(f"  Cost to build ALL routes:    ${total_cost}M")
    print(f"  Cost with Boruvka's MST:     ${mst_cost}M")
    print(f"  Infrastructure Savings:      ${total_cost - mst_cost}M ({savings_pct:.1f}%)")
    print_separator()
    print()


def display_network_statistics(graph, mst_edges):
    """
    Display detailed MST statistics.

    Args:
        graph: Original graph.
        mst_edges: MST edges.
    """
    stats = get_mst_statistics(graph, mst_edges)

    print("NETWORK STATISTICS")
    print_separator()
    print(f"  Total Hubs Connected:        {stats['num_vertices']}")
    print(f"  Cables in MST:               {stats['num_mst_edges']}")
    print(f"  MST Diameter (max path):     ${stats['mst_diameter']}M")
    print(f"  Cheapest Cable:              ${stats['min_edge_weight']}M")
    print(f"  Most Expensive Cable:        ${stats['max_edge_weight']}M")
    print(f"  Average Cable Cost:          ${stats['avg_edge_weight']:.1f}M")
    print_separator()
    print()


def display_algorithm_insight():
    """Display educational note about Borůvka's component-merging strategy."""
    print("ALGORITHM INSIGHT: BORUVKA'S COMPONENT MERGING")
    print_separator()
    print("  Unlike Kruskal's (sort all edges) or Prim's (grow one tree),")
    print("  Boruvka's works in ROUNDS:")
    print()
    print("    Round 1: Each hub independently picks its cheapest link")
    print("    Round 2: Each merged region picks its cheapest cross-region link")
    print("    Round 3: Repeat until all hubs are connected")
    print()
    print("  Components halve each round -> O(log V) rounds total")
    print("  Each round's searches are INDEPENDENT -> parallelizable!")
    print_separator()
    print()


def run_network_optimization():
    """Main function: run the global network optimization simulation."""
    clear_screen()
    print_header()

    # Load network data
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data = load_network_data(os.path.join(script_dir, 'network_data.json'))
    if not data:
        return

    # Build graph
    graph = build_graph_from_data(data)

    # Display input summary
    display_network_summary(data, graph)

    # Run Borůvka's Algorithm
    print("Executing Boruvka's MST Algorithm...")
    print()
    mst_edges, total_cost = boruvkas_mst(graph)

    # Display results
    display_mst_result(mst_edges, total_cost)
    display_savings_analysis(graph, mst_edges)
    display_network_statistics(graph, mst_edges)
    display_algorithm_insight()

    print("STATUS: Every data center hub is now connected with zero cycles.")
    print("        Network is ready for deployment.")
    print("=" * 70)


if __name__ == "__main__":
    run_network_optimization()
