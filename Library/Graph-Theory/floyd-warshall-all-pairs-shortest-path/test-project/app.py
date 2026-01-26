import sys
import os

# Add the parent directory to the path so we can import the core logic
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.floyd_warshall import (
    floyd_warshall, reconstruct_path, get_graph_diameter,
    get_graph_center, detect_negative_cycle, transitive_closure
)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_city_network(filename='city_network.txt'):
    """Load city network from file."""
    graph = {}
    cities = set()
    
    # Check if file exists, if not create with default data
    if not os.path.exists(filename):
        create_default_network_file(filename)
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            parts = line.split()
            if len(parts) != 3:
                continue
            
            from_city, to_city, cost = parts[0], parts[1], float(parts[2])
            
            cities.add(from_city)
            cities.add(to_city)
            
            if from_city not in graph:
                graph[from_city] = {}
            graph[from_city][to_city] = cost
    
    # Ensure all cities have an entry (even if no outgoing edges)
    for city in cities:
        if city not in graph:
            graph[city] = {}
    
    return graph, cities

def create_default_network_file(filename):
    """Create a default city network file."""
    default_data = """# City Transportation Network (Format: FROM TO COST)
# Example: NYC BOS 215 means NYC to Boston costs 215 (km, time, or $)

# East Coast Cities
NYC BOS 215
NYC PHI 95
BOS NYC 220
PHI NYC 100
PHI DC 140
DC PHI 145
BOS PHI 300

# West Coast Connection
NYC LA 2800
LA SF 380
SF LA 385
LA LV 270
LV LA 275
SF SEA 810
SEA SF 815

# Central Hub
CHI NYC 790
NYC CHI 785
CHI LA 2015
LA CHI 2010
CHI SEA 2015

# Add your own cities below:
"""
    with open(filename, 'w') as f:
        f.write(default_data)

def display_distance_matrix(distances, cities):
    """Display distance matrix in tabular format."""
    cities_list = sorted(cities)
    
    # Header
    print("     ", end="")
    for city in cities_list:
        print(f"{city:>8}", end="")
    print()
    
    # Separator
    print("     " + "-" * (8 * len(cities_list)))
    
    # Rows
    for from_city in cities_list:
        print(f"{from_city:>4}|", end="")
        for to_city in cities_list:
            dist = distances[(from_city, to_city)]
            if dist == float('inf'):
                print(f"{'∞':>8}", end="")
            else:
                print(f"{dist:>8.0f}", end="")
        print()

def analyze_network():
    """Main network analysis function."""
    clear_screen()
    
    print("=" * 75)
    print(" CITY LOGISTICS NETWORK ANALYZER: Floyd-Warshall Algorithm")
    print("=" * 75)
    print()
    print("SCENARIO: You manage a logistics company with multiple city hubs.")
    print("You need to optimize routes, find the best hub location, and analyze")
    print("the network's connectivity and efficiency.")
    print()
    print("-" * 75)
    
    # Load network
    graph, cities = load_city_network()
    
    print(f"\n✓ Loaded network with {len(cities)} cities")
    print(f"  Cities: {', '.join(sorted(cities))}")
    print()
    
    print("🔄 Running Floyd-Warshall algorithm...")
    
    # Run Floyd-Warshall
    distances, next_node = floyd_warshall(graph)
    
    print("✓ Computation complete!\n")
    
    # Check for negative cycles
    if detect_negative_cycle(graph, distances):
        print("⚠️  WARNING: Negative cycle detected in the network!")
        print("    This indicates an impossible situation (e.g., cost reduction loop).\n")
        return
    
    while True:
        print("-" * 75)
        print("\nANALYSIS OPTIONS:")
        print("1. Show complete distance matrix")
        print("2. Find shortest route between two cities")
        print("3. Find optimal hub location (graph center)")
        print("4. Calculate network diameter")
        print("5. Check city connectivity (reachability)")
        print("6. Show all routes from a city")
        print("7. Return to main menu")
        print()
        
        choice = input("Select option (1-7): ").strip()
        
        if choice == '1':
            print("\n📊 COMPLETE DISTANCE MATRIX:")
            print("   (Shows shortest distance from each city to every other city)\n")
            display_distance_matrix(distances, cities)
            print()
        
        elif choice == '2':
            print()
            from_city = input("From city: ").strip().upper()
            to_city = input("To city: ").strip().upper()
            
            if from_city not in cities or to_city not in cities:
                print(f"\n⚠️  Unknown city. Available: {', '.join(sorted(cities))}")
                continue
            
            dist = distances[(from_city, to_city)]
            if dist == float('inf'):
                print(f"\n❌ No route exists from {from_city} to {to_city}")
            else:
                path = reconstruct_path(next_node, from_city, to_city)
                print(f"\n✓ Shortest route from {from_city} to {to_city}:")
                print(f"  Distance: {dist:.0f}")
                print(f"  Path: {' → '.join(path)}")
            print()
        
        elif choice == '3':
            print("\n🎯 FINDING OPTIMAL HUB LOCATION...")
            print("   (City that minimizes maximum distance to other cities)\n")
            
            center, eccentricity = get_graph_center(graph)
            
            if center:
                print(f"✓ Optimal hub: {center}")
                print(f"  Maximum distance to any city: {eccentricity:.0f}")
                print(f"\n  Interpretation: Placing your main warehouse in {center}")
                print(f"  ensures no destination is farther than {eccentricity:.0f} units away.")
            else:
                print("❌ Unable to determine center (disconnected network)")
            print()
        
        elif choice == '4':
            print("\n📏 CALCULATING NETWORK DIAMETER...")
            print("   (Longest shortest path in the network)\n")
            
            diameter = get_graph_diameter(graph)
            
            if diameter == float('inf'):
                print("❌ Network is disconnected (some cities unreachable)")
            else:
                print(f"✓ Network diameter: {diameter:.0f}")
                print(f"\n  Interpretation: The worst-case distance between any two")
                print(f"  connected cities is {diameter:.0f} units.")
            print()
        
        elif choice == '5':
            print("\n🔗 CITY CONNECTIVITY ANALYSIS (Transitive Closure)...\n")
            
            reach = transitive_closure(graph)
            
            print("Reachability Matrix (✓ = can reach, ✗ = cannot reach):\n")
            cities_list = sorted(cities)
            
            # Header
            print("     ", end="")
            for city in cities_list:
                print(f"{city:>5}", end="")
            print()
            
            # Rows
            for from_city in cities_list:
                print(f"{from_city:>4}|", end="")
                for to_city in cities_list:
                    symbol = "✓" if reach[(from_city, to_city)] else "✗"
                    print(f"{symbol:>5}", end="")
                print()
            
            # Summary
            total_pairs = len(cities) * (len(cities) - 1)
            reachable = sum(1 for (i, j), r in reach.items() if i != j and r)
            connectivity = (reachable / total_pairs * 100) if total_pairs > 0 else 0
            
            print(f"\n  Network Connectivity: {connectivity:.1f}%")
            print(f"  ({reachable}/{total_pairs} city pairs are connected)")
            print()
        
        elif choice == '6':
            print()
            source = input("Source city: ").strip().upper()
            
            if source not in cities:
                print(f"\n⚠️  Unknown city. Available: {', '.join(sorted(cities))}")
                continue
            
            print(f"\n📍 ALL ROUTES FROM {source}:\n")
            
            destinations = sorted(cities - {source})
            for dest in destinations:
                dist = distances[(source, dest)]
                if dist == float('inf'):
                    print(f"  {dest:>4}: No route available")
                else:
                    path = reconstruct_path(next_node, source, dest)
                    path_str = ' → '.join(path)
                    print(f"  {dest:>4}: {dist:>6.0f} via {path_str}")
            print()
        
        elif choice == '7':
            break
        
        else:
            print("\n⚠️  Invalid option. Please select 1-7.\n")
        
        input("Press Enter to continue...")
        print()

def manual_network():
    """Allow user to manually build a network."""
    clear_screen()
    
    print("=" * 75)
    print(" MANUAL NETWORK BUILDER")
    print("=" * 75)
    print()
    
    graph = {}
    cities = set()
    
    print("Build your own city network!")
    print("Enter connections (format: FROM TO COST)")
    print("Example: NYC BOS 215")
    print("Type 'done' when finished\n")
    
    while True:
        entry = input("Connection: ").strip()
        
        if entry.lower() == 'done':
            break
        
        parts = entry.split()
        if len(parts) != 3:
            print("  ⚠️  Invalid format. Use: FROM TO COST")
            continue
        
        try:
            from_city, to_city, cost = parts[0].upper(), parts[1].upper(), float(parts[2])
            
            cities.add(from_city)
            cities.add(to_city)
            
            if from_city not in graph:
                graph[from_city] = {}
            graph[from_city][to_city] = cost
            
            print(f"  ✓ Added: {from_city} → {to_city} = {cost}")
        
        except ValueError:
            print("  ⚠️  Invalid cost value")
    
    if not cities:
        print("\nNo network created.")
        return
    
    # Ensure all cities have entries
    for city in cities:
        if city not in graph:
            graph[city] = {}
    
    print(f"\n✓ Network created with {len(cities)} cities\n")
    print("🔄 Running Floyd-Warshall...")
    
    distances, next_node = floyd_warshall(graph)
    
    print("✓ Analysis complete!\n")
    print("📊 DISTANCE MATRIX:\n")
    
    display_distance_matrix(distances, cities)
    print()

def main_menu():
    """Main application menu."""
    while True:
        clear_screen()
        
        print("=" * 75)
        print(" FLOYD-WARSHALL NETWORK ANALYZER")
        print("=" * 75)
        print()
        print("1. Analyze city network from file (city_network.txt)")
        print("2. Build custom network manually")
        print("3. Exit")
        print()
        
        choice = input("Select option (1-3): ").strip()
        
        if choice == '1':
            analyze_network()
        
        elif choice == '2':
            manual_network()
            input("\nPress Enter to continue...")
        
        elif choice == '3':
            print("\nThank you for using the Network Analyzer!")
            break
        
        else:
            print("\n⚠️  Invalid option. Please select 1-3.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nExiting...")
