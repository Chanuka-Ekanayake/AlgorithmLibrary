import sys
import os

# Add the parent directory to the path so we can import the core logic
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.dijkstra import get_shortest_path, reconstruct_path

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def interactive_simulation():
    clear_screen()
    print("==============================================")
    print(" REAL-WORLD LOGISTICS: DIJKSTRA OPTIMIZER ")
    print("==============================================\n")
    
    print("SCENARIO: You are the Lead Engineer for an E-commerce Delivery Startup.")
    print("You need to find the fastest route through a city's traffic.\n")

    # --- Step 1: Get User Inputs for the Map ---
    city_map = {}
    print("--- 1. BUILD YOUR CITY MAP ---")
    while True:
        node = input("Enter a Location Name (or type 'done' to finish): ").strip()
        if node.lower() == 'done': break
        
        city_map[node] = {}
        print(f"Adding connections for {node}...")
        
        while True:
            neighbor = input(f"  -> Connect {node} to which neighbor? (or 'next' for new location): ").strip()
            if neighbor.lower() == 'next': break
            
            try:
                weight = float(input(f"  -> Minutes/Cost to travel from {node} to {neighbor}: "))
                city_map[node][neighbor] = weight
            except ValueError:
                print("  ⚠️ Please enter a numeric value for the cost.")

    if not city_map:
        print(" Map is empty. Exiting.")
        return

    # --- Step 2: Choose Start and End ---
    clear_screen()
    print("--- 2. DEFINE THE DELIVERY MISSION ---")
    print(f"Available Locations: {', '.join(city_map.keys())}")
    
    start_point = input("\nEnter the Starting Warehouse: ").strip()
    end_point = input("Enter the Customer Destination: ").strip()

    if start_point not in city_map or end_point not in city_map:
        print("Error: Locations not found in your map.")
        return

    # --- Step 3: Run the Core Algorithm ---
    print("\n--- 3. CALCULATING OPTIMAL ROUTE... ---")
    costs, parents = get_shortest_path(city_map, start_point)
    
    if costs[end_point] == float('inf'):
        print(f"⚠️ Oh no! No path exists between {start_point} and {end_point}.")
    else:
        route = reconstruct_path(parents, end_point)
        
        print("\nMISSION SUCCESSFUL!")
        print(f"Best Route: {' ➔ '.join(route)}")
        print(f"Total Travel Time: {costs[end_point]} minutes")
        
        # Educational Breakdown
        print("\n--- HOW DIJKSTRA DECIDED THIS: ---")
        print(f"1. It started at {start_point} with a cost of 0.")
        print("2. It explored neighbors greedily, always picking the 'cheapest' next step.")
        print(f"3. It found that going through {route[1] if len(route) > 2 else 'the direct path'} was more efficient than other options.")

if __name__ == "__main__":
    interactive_simulation()