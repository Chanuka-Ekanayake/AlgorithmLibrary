"""
Real-World Application: Network Vulnerability Analysis
Uses Articulation Points and Bridges to identify critical network components
"""

import sys
import os

# Add parent directory to path to import the core module
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.articulation_points import (
    ArticulationPointsAndBridges,
    find_critical_connections_with_names,
    analyze_network_vulnerability
)


def computer_network_analysis():
    """
    Example: Corporate Computer Network
    Identify critical routers and connections in office network
    """
    print("=" * 70)
    print("COMPUTER NETWORK - Critical Infrastructure Analysis")
    print("=" * 70)
    
    # Network topology
    routers = [
        "Gateway",           # 0 - Main internet gateway
        "Floor1_Switch",     # 1 - Floor 1 central switch
        "Floor2_Switch",     # 2 - Floor 2 central switch
        "ServerRoom",        # 3 - Server room
        "Dev_Zone",          # 4 - Development area
        "Sales_Zone",        # 5 - Sales area
        "HR_Zone",           # 6 - HR area
        "Backup_Link"        # 7 - Backup connection
    ]
    
    # Network connections (undirected)
    connections = [
        ("Gateway", "Floor1_Switch"),
        ("Gateway", "Floor2_Switch"),
        ("Floor1_Switch", "ServerRoom"),
        ("Floor1_Switch", "Dev_Zone"),
        ("Floor2_Switch", "Sales_Zone"),
        ("Floor2_Switch", "HR_Zone"),
        ("ServerRoom", "Backup_Link"),
        ("Dev_Zone", "Backup_Link"),
    ]
    
    print("\nNetwork Topology:")
    print("  Routers:", ", ".join(routers))
    print("\n  Connections:")
    for src, dst in connections:
        print(f"    {src} <---> {dst}")
    
    # Analyze vulnerability
    analysis = analyze_network_vulnerability(routers, connections)
    
    print("\n" + "─" * 70)
    print("VULNERABILITY ANALYSIS")
    print("─" * 70)
    
    print(f"\n🔴 Critical Routers (Articulation Points):")
    if analysis['articulation_points']:
        for router in analysis['articulation_points']:
            print(f"  ⚠️  {router}")
            print(f"      → Failure would partition the network")
    else:
        print("  ✓ No single point of failure detected")
    
    print(f"\n🔴 Critical Connections (Bridges):")
    if analysis['bridges']:
        for src, dst in analysis['bridges']:
            print(f"  ⚠️  {src} <---> {dst}")
            print(f"      → Failure would isolate network segments")
    else:
        print("  ✓ All connections have redundancy")
    
    stats = analysis['statistics']
    print(f"\n📊 Network Statistics:")
    print(f"  Total Routers: {stats['total_nodes']}")
    print(f"  Total Connections: {stats['total_edges']}")
    print(f"  Critical Routers: {stats['critical_nodes']} ({stats['node_vulnerability_percentage']}%)")
    print(f"  Critical Connections: {stats['critical_edges']} ({stats['edge_vulnerability_percentage']}%)")
    
    print("\n💡 Recommendations:")
    if stats['node_vulnerability_percentage'] > 30:
        print("  ⚠️  HIGH RISK: Add redundant routers to critical points")
    if stats['edge_vulnerability_percentage'] > 30:
        print("  ⚠️  HIGH RISK: Add redundant connections between segments")
    if stats['critical_nodes'] == 0 and stats['critical_edges'] == 0:
        print("  ✓ Network has good redundancy design")


def transportation_network_analysis():
    """
    Example: City Transportation Network
    Identify critical intersections and roads
    """
    print("\n\n" + "=" * 70)
    print("TRANSPORTATION NETWORK - Critical Infrastructure")
    print("=" * 70)
    
    intersections = [
        "Downtown",          # 0
        "Airport",           # 1
        "Hospital",          # 2
        "University",        # 3
        "Shopping_Mall",     # 4
        "Train_Station",     # 5
        "Industrial_Zone",   # 6
        "Residential_East",  # 7
        "Residential_West"   # 8
    ]
    
    roads = [
        ("Downtown", "Airport"),
        ("Downtown", "Hospital"),
        ("Downtown", "Shopping_Mall"),
        ("Hospital", "University"),
        ("University", "Train_Station"),
        ("Shopping_Mall", "Residential_East"),
        ("Train_Station", "Industrial_Zone"),
        ("Industrial_Zone", "Residential_West"),
        ("Airport", "Train_Station"),
    ]
    
    print("\nCity Map:")
    print("  Intersections:", len(intersections))
    print("  Roads:", len(roads))
    
    # Find critical points
    graph = ArticulationPointsAndBridges(len(intersections))
    intersection_map = {name: i for i, name in enumerate(intersections)}
    
    for src, dst in roads:
        graph.add_edge(intersection_map[src], intersection_map[dst])
    
    ap_indices = graph.find_articulation_points()
    bridges = graph.find_bridges()
    
    critical_intersections = [intersections[i] for i in ap_indices]
    critical_roads = [(intersections[u], intersections[v]) for u, v in bridges]
    
    print("\n" + "─" * 70)
    print("CRITICAL INFRASTRUCTURE ANALYSIS")
    print("─" * 70)
    
    print("\n🚦 Critical Intersections:")
    if critical_intersections:
        for intersection in critical_intersections:
            print(f"  ⚠️  {intersection}")
            print(f"      → Closure would isolate city areas")
    else:
        print("  ✓ All intersections have alternate routes")
    
    print("\n🛣️  Critical Roads:")
    if critical_roads:
        for src, dst in critical_roads:
            print(f"  ⚠️  {src} ↔ {dst}")
            print(f"      → Closure would require long detours")
    else:
        print("  ✓ All roads have alternate routes")
    
    print("\n💡 Urban Planning Recommendations:")
    if critical_intersections:
        print("  • Construct bypass roads around critical intersections")
        print("  • Increase traffic flow capacity at bottleneck points")
    if critical_roads:
        print("  • Build parallel routes for critical roads")
        print("  • Establish emergency detour plans")


def social_network_analysis():
    """
    Example: Social Network Community Structure
    Find key influencers connecting different groups
    """
    print("\n\n" + "=" * 70)
    print("SOCIAL NETWORK - Key Influencer Analysis")
    print("=" * 70)
    
    people = [
        "Alice",    # 0 - Connects Tech & Marketing
        "Bob",      # 1 - Tech team
        "Carol",    # 2 - Tech team
        "David",    # 3 - Marketing team
        "Eve",      # 4 - Marketing team
        "Frank",    # 5 - Connects Marketing & Sales
        "Grace",    # 6 - Sales team
        "Henry",    # 7 - Sales team
    ]
    
    friendships = [
        ("Alice", "Bob"),
        ("Alice", "Carol"),
        ("Alice", "David"),
        ("Bob", "Carol"),
        ("David", "Eve"),
        ("David", "Frank"),
        ("Eve", "Frank"),
        ("Frank", "Grace"),
        ("Frank", "Henry"),
        ("Grace", "Henry"),
    ]
    
    print("\nSocial Network:")
    print("  People:", len(people))
    print("  Friendships:", len(friendships))
    
    result = find_critical_connections_with_names(people, friendships)
    
    print("\n" + "─" * 70)
    print("INFLUENCER ANALYSIS")
    print("─" * 70)
    
    print("\n👥 Key Influencers (Bridge Different Communities):")
    if result['articulation_points']:
        for person in result['articulation_points']:
            print(f"  ⭐ {person}")
            print(f"      → Connects separate social groups")
    else:
        print("  • Network is tightly connected")
    
    print("\n🔗 Critical Friendships:")
    if result['bridges']:
        for p1, p2 in result['bridges']:
            print(f"  • {p1} ↔ {p2}")
            print(f"      → Only connection between groups")
    else:
        print("  • Multiple connections between all groups")
    
    print("\n💡 Marketing Strategy:")
    if result['articulation_points']:
        print(f"  • Target these {len(result['articulation_points'])} influencers for viral marketing")
        print("  • Information spreads through them to reach all communities")


def power_grid_analysis():
    """
    Example: Electrical Power Grid
    Identify critical substations and transmission lines
    """
    print("\n\n" + "=" * 70)
    print("POWER GRID - Infrastructure Vulnerability")
    print("=" * 70)
    
    substations = [
        "Main_Plant",        # 0 - Primary power generation
        "Substation_A",      # 1 - Distribution hub
        "Substation_B",      # 2 - Distribution hub
        "Industrial_Feed",   # 3 - Industrial area
        "Residential_N",     # 4 - North residential
        "Residential_S",     # 5 - South residential
        "Hospital_Feed",     # 6 - Critical hospital
        "Backup_Gen",        # 7 - Backup generator
    ]
    
    transmission_lines = [
        ("Main_Plant", "Substation_A"),
        ("Main_Plant", "Substation_B"),
        ("Substation_A", "Industrial_Feed"),
        ("Substation_A", "Residential_N"),
        ("Substation_B", "Residential_S"),
        ("Substation_B", "Hospital_Feed"),
        ("Industrial_Feed", "Backup_Gen"),
    ]
    
    print("\nPower Grid Configuration:")
    print("  Substations:", len(substations))
    print("  Transmission Lines:", len(transmission_lines))
    
    analysis = analyze_network_vulnerability(substations, transmission_lines)
    
    print("\n" + "─" * 70)
    print("VULNERABILITY ASSESSMENT")
    print("─" * 70)
    
    print("\n⚡ Critical Substations:")
    if analysis['articulation_points']:
        for station in analysis['articulation_points']:
            print(f"  🔴 {station}")
            print(f"      → Failure causes widespread outage")
    else:
        print("  ✓ Grid has N-1 redundancy")
    
    print("\n⚡ Critical Transmission Lines:")
    if analysis['bridges']:
        for src, dst in analysis['bridges']:
            print(f"  🔴 {src} ←→ {dst}")
            print(f"      → Failure isolates power zones")
    else:
        print("  ✓ All lines have backup routes")
    
    stats = analysis['statistics']
    print(f"\n📊 Grid Reliability Metrics:")
    print(f"  Grid Resilience: {100 - stats['node_vulnerability_percentage']:.1f}%")
    print(f"  Line Redundancy: {100 - stats['edge_vulnerability_percentage']:.1f}%")
    
    print("\n💡 Infrastructure Hardening Plan:")
    if stats['critical_nodes'] > 0:
        print("  1. Install backup transformers at critical substations")
        print("  2. Upgrade capacity of critical distribution points")
    if stats['critical_edges'] > 0:
        print("  3. Build redundant transmission lines")
        print("  4. Deploy mobile substations for emergency backup")
    
    if stats['node_vulnerability_percentage'] < 20:
        print("  ✓ Grid meets N-1 contingency standards")


def simple_example():
    """
    Example: Simple Graph Demonstration
    Visual representation of algorithm behavior
    """
    print("\n\n" + "=" * 70)
    print("SIMPLE DEMONSTRATION - Algorithm Visualization")
    print("=" * 70)
    
    print("\nGraph Structure:")
    print("""
        0 ─── 1 ─── 2
        │     │
        3 ─── 4
        
    Vertices: 0, 1, 2, 3, 4
    Edges: (0,1), (0,3), (1,2), (1,4), (3,4)
    """)
    
    # Create graph
    graph = ArticulationPointsAndBridges(5)
    graph.add_edge(0, 1)
    graph.add_edge(0, 3)
    graph.add_edge(1, 2)
    graph.add_edge(1, 4)
    graph.add_edge(3, 4)
    
    # Find critical components
    ap = graph.find_articulation_points()
    bridges = graph.find_bridges()
    
    print("Analysis Results:")
    print(f"\n  Articulation Points: {ap}")
    print("    → Vertex 1: Articulation point; removing it isolates vertex 2")
    
    
    print(f"\n  Bridges: {bridges}")
    print("    → Edge (1,2): Only connection to vertex 2")
    
    print("\n  Removing vertex 0: Graph remains connected (vertices {1,2,3,4})")
    print("  Removing vertex 1: Vertex 2 becomes isolated")
    print("  Removing edge (1,2): Vertex 2 becomes isolated")


def main():
    """Run all examples"""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 8 + "ARTICULATION POINTS & BRIDGES ALGORITHM" + " " * 20 + "║")
    print("║" + " " * 12 + "Critical Connection Analysis" + " " * 28 + "║")
    print("╚" + "═" * 68 + "╝")
    
    # Run all demonstrations
    computer_network_analysis()
    transportation_network_analysis()
    social_network_analysis()
    power_grid_analysis()
    simple_example()
    
    print("\n" + "=" * 70)
    print("All analyses completed!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
