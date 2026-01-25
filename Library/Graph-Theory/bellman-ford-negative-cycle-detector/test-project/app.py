import sys
import os
import math

# Add the parent directory to the path so we can import the core logic
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.bellman_ford import bellman_ford, reconstruct_path, detect_negative_cycle_nodes

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_exchange_rates(filename='exchange_rates.txt'):
    """Load currency exchange rates from file."""
    graph = {}
    currencies = set()
    
    # Check if file exists, if not create with default data
    if not os.path.exists(filename):
        create_default_exchange_file(filename)
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            parts = line.split()
            if len(parts) != 3:
                continue
            
            from_curr, to_curr, rate = parts[0], parts[1], float(parts[2])
            
            currencies.add(from_curr)
            currencies.add(to_curr)
            
            # Convert exchange rate to negative log for arbitrage detection
            # log transformation: multiplication becomes addition
            # Arbitrage exists if product > 1, i.e., sum of logs > 0, i.e., sum of -logs < 0
            weight = -math.log(rate)
            
            if from_curr not in graph:
                graph[from_curr] = []
            graph[from_curr].append((to_curr, weight))
    
    # Ensure all currencies have an entry (even if empty)
    for curr in currencies:
        if curr not in graph:
            graph[curr] = []
    
    return graph, currencies

def create_default_exchange_file(filename):
    """Create a default exchange rates file with sample data."""
    default_data = """# Currency Exchange Rates (Format: FROM TO RATE)
# Example: USD EUR 0.85 means 1 USD = 0.85 EUR

USD EUR 0.85
EUR GBP 0.90
GBP USD 1.30

USD JPY 110.0
JPY EUR 0.0078
EUR USD 1.18

USD CAD 1.25
CAD GBP 0.60
GBP CAD 1.65

# Add your own rates below:
"""
    with open(filename, 'w') as f:
        f.write(default_data)

def detect_arbitrage():
    """Main arbitrage detection simulation."""
    clear_screen()
    
    print("=" * 70)
    print(" CURRENCY ARBITRAGE DETECTOR: Bellman-Ford Algorithm")
    print("=" * 70)
    print()
    print("SCENARIO: You are a quantitative trader analyzing foreign exchange")
    print("markets for arbitrage opportunities. An arbitrage exists when you can")
    print("profit by converting currencies in a cycle.")
    print()
    print("Example: USD → EUR → GBP → USD with a net profit")
    print()
    print("-" * 70)
    
    # Load exchange rates
    graph, currencies = load_exchange_rates()
    
    print(f"\n✓ Loaded {len(currencies)} currencies with exchange rate data")
    print(f"  Currencies: {', '.join(sorted(currencies))}")
    print()
    
    # Choose a starting currency
    start_currency = input("Enter starting currency (or press Enter for USD): ").strip().upper()
    if not start_currency or start_currency not in currencies:
        start_currency = 'USD'
    
    print(f"\n🔍 Analyzing arbitrage opportunities from {start_currency}...\n")
    
    # Run Bellman-Ford
    distances, predecessors, has_negative_cycle = bellman_ford(graph, start_currency)
    
    if has_negative_cycle:
        print("🎉 ARBITRAGE OPPORTUNITY DETECTED! 🎉\n")
        print("A negative cycle exists, meaning you can profit from currency conversion.")
        print()
        
        # Find the cycle
        cycle_nodes = detect_negative_cycle_nodes(graph, start_currency)
        
        if cycle_nodes:
            print(f"💰 Arbitrage Cycle Found:")
            print(f"   {' → '.join(cycle_nodes)} → {cycle_nodes[0]}")
            print()
            
            # Calculate the actual profit
            print("📊 Conversion Analysis:")
            profit_multiplier = 1.0
            
            for i in range(len(cycle_nodes)):
                from_curr = cycle_nodes[i]
                to_curr = cycle_nodes[(i + 1) % len(cycle_nodes)]
                
                # Find the exchange rate
                for neighbor, weight in graph[from_curr]:
                    if neighbor == to_curr:
                        rate = math.exp(-weight)
                        profit_multiplier *= rate
                        print(f"   {from_curr} → {to_curr}: {rate:.6f}")
                        break
            
            profit_percent = (profit_multiplier - 1) * 100
            print()
            print(f"✨ Net Result: 1.00 → {profit_multiplier:.6f}")
            print(f"   Profit: {profit_percent:+.4f}% per cycle")
            print()
            
            if profit_percent > 0:
                print("⚠️  This is a profitable arbitrage! (In theory)")
                print("    Real markets: Transaction fees and latency typically eliminate arbitrage.")
            else:
                print("ℹ️  Negative cycle detected but no profit (computational precision issue)")
    
    else:
        print("✓ No arbitrage opportunities detected.\n")
        print("All currency conversion cycles result in a loss or break-even.")
        print()
        
        # Show shortest "distance" to each currency
        print("📈 Optimal Conversion Rates from", start_currency, ":\n")
        
        sorted_currencies = sorted(currencies - {start_currency})
        for curr in sorted_currencies:
            if distances[curr] != float('inf'):
                # Convert back from log space
                rate = math.exp(-distances[curr])
                path = reconstruct_path(predecessors, start_currency, curr)
                
                if path and len(path) > 1:
                    path_str = ' → '.join(path)
                    print(f"   {curr}: {rate:.6f}  (via {path_str})")
                else:
                    print(f"   {curr}: {rate:.6f}")
        
        print()
    
    print("-" * 70)

def manual_mode():
    """Allow user to manually add exchange rates and test."""
    clear_screen()
    
    print("=" * 70)
    print(" MANUAL EXCHANGE RATE INPUT")
    print("=" * 70)
    print()
    
    graph = {}
    currencies = set()
    
    print("Enter exchange rates (format: FROM TO RATE)")
    print("Example: USD EUR 0.85")
    print("Type 'done' when finished\n")
    
    while True:
        entry = input("Exchange rate: ").strip()
        
        if entry.lower() == 'done':
            break
        
        parts = entry.split()
        if len(parts) != 3:
            print("  ⚠️  Invalid format. Use: FROM TO RATE")
            continue
        
        try:
            from_curr, to_curr, rate = parts[0].upper(), parts[1].upper(), float(parts[2])
            
            if rate <= 0:
                print("  ⚠️  Rate must be positive")
                continue
            
            currencies.add(from_curr)
            currencies.add(to_curr)
            
            weight = -math.log(rate)
            
            if from_curr not in graph:
                graph[from_curr] = []
            graph[from_curr].append((to_curr, weight))
            
            print(f"  ✓ Added: {from_curr} → {to_curr} = {rate}")
        
        except ValueError:
            print("  ⚠️  Invalid rate value")
    
    if not currencies:
        print("\nNo exchange rates entered.")
        return
    
    # Ensure all currencies have entries
    for curr in currencies:
        if curr not in graph:
            graph[curr] = []
    
    start = input(f"\nStarting currency ({', '.join(sorted(currencies))}): ").strip().upper()
    if start not in currencies:
        start = list(currencies)[0]
    
    print(f"\n🔍 Analyzing from {start}...\n")
    
    distances, predecessors, has_cycle = bellman_ford(graph, start)
    
    if has_cycle:
        print("🎉 ARBITRAGE DETECTED!\n")
        cycle = detect_negative_cycle_nodes(graph, start)
        if cycle:
            print(f"Cycle: {' → '.join(cycle)} → {cycle[0]}")
    else:
        print("✓ No arbitrage opportunities found.\n")

def main_menu():
    """Main application menu."""
    while True:
        clear_screen()
        
        print("=" * 70)
        print(" BELLMAN-FORD ARBITRAGE DETECTOR")
        print("=" * 70)
        print()
        print("1. Detect arbitrage from file (exchange_rates.txt)")
        print("2. Manual exchange rate input")
        print("3. Exit")
        print()
        
        choice = input("Select option (1-3): ").strip()
        
        if choice == '1':
            detect_arbitrage()
            input("\nPress Enter to continue...")
        
        elif choice == '2':
            manual_mode()
            input("\nPress Enter to continue...")
        
        elif choice == '3':
            print("\nThank you for using the Arbitrage Detector!")
            break
        
        else:
            print("\n⚠️  Invalid option. Please select 1-3.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nExiting...")
