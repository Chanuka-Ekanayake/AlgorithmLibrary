import sys
import os

# Allow importing from the parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.johnsons import (
    johnsons, reconstruct_path, detect_negative_cycle,
    get_distance_matrix, get_graph_diameter, get_graph_center
)


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def separator(char='=', width=72):
    print(char * width)


def print_header(title: str):
    separator()
    print(f"  {title}")
    separator()
    print()


def display_distance_matrix(distances, vertices):
    """Display all-pairs distance matrix in tabular form."""
    v_list = sorted(vertices)
    col_w = 9

    # Header row
    print(f"{'':>6}", end="")
    for v in v_list:
        print(f"{v:>{col_w}}", end="")
    print()
    print("      " + "─" * (col_w * len(v_list)))

    for src in v_list:
        print(f"{src:>5}│", end="")
        for dst in v_list:
            d = distances.get((src, dst), float('inf'))
            if d == float('inf'):
                print(f"{'∞':>{col_w}}", end="")
            else:
                print(f"{d:>{col_w}.1f}", end="")
        print()


# ─────────────────────────────────────────────────────────────────────────────
# SCENARIO 1 — Intercity Network with Discount Routes (negative edge = subsidy)
# ─────────────────────────────────────────────────────────────────────────────

def scenario_intercity_network():
    clear_screen()
    print_header("INTERCITY TRANSPORT NETWORK  —  Johnson's Algorithm")

    print("SCENARIO:")
    print("  A regional transport authority manages routes between 6 cities.")
    print("  Some routes have government subsidies (negative cost = subsidy).")
    print("  Find the cheapest travel cost between ALL city pairs.\n")
    separator('-')

    # Costs in €, subsidised routes have negative cost
    graph = {
        'Athens':   {'Berlin': 120,  'Cairo': 80},
        'Berlin':   {'Cairo': -30,   'Dublin': 50},
        'Cairo':    {'Dublin': 40,   'Edinburgh': 90},
        'Dublin':   {'Edinburgh': 20},
        'Edinburgh':{'Frankfurt': 60},
        'Frankfurt':{'Athens': 100},
    }

    cities = set(graph.keys()) | {v for nbrs in graph.values() for v in nbrs}

    print(f"  Cities: {', '.join(sorted(cities))}")
    print(f"  Routes: {sum(len(v) for v in graph.values())}")
    print(f"  Includes subsidised (negative cost) route: Berlin → Cairo (−€30)\n")

    if detect_negative_cycle(graph):
        print("  ⚠️  Negative cycle detected — no valid shortest paths.\n")
        return

    distances, next_node = johnsons(graph)

    print("  📊 All-pairs cheapest travel cost matrix (€):\n")
    display_distance_matrix(distances, cities)

    print("\n  📍 Sample cheapest routes:")
    pairs = [('Athens', 'Edinburgh'), ('Berlin', 'Frankfurt'), ('Cairo', 'Athens')]
    for src, dst in pairs:
        d = distances.get((src, dst), float('inf'))
        path = reconstruct_path(next_node, src, dst)
        if path:
            print(f"    {src} → {dst}: €{d:.0f}  via  {' → '.join(path)}")
        else:
            print(f"    {src} → {dst}: unreachable")

    print()
    input("  Press Enter to continue...\n")


# ─────────────────────────────────────────────────────────────────────────────
# SCENARIO 2 — Software Build Dependency (task with time-savings / shortcuts)
# ─────────────────────────────────────────────────────────────────────────────

def scenario_build_pipeline():
    clear_screen()
    print_header("SOFTWARE BUILD PIPELINE OPTIMIZER  —  Johnson's Algorithm")

    print("SCENARIO:")
    print("  A CI/CD system models build steps as a directed graph.")
    print("  Edge weight = time in seconds (negative = caching shortcut).")
    print("  Minimise the total build time from any step to any other.\n")
    separator('-')

    graph = {
        'Checkout': {'Lint': 5,    'Test': 12},
        'Lint':     {'Build': 8,   'Test': -2},   # Lint result cached → shortcut
        'Test':     {'Build': 3},
        'Build':    {'Package': 4, 'Docs': 6},
        'Package':  {'Deploy': 2},
        'Docs':     {'Deploy': 1},
        'Deploy':   {},
    }

    steps = set(graph.keys()) | {v for nbrs in graph.values() for v in nbrs}
    print(f"  Build steps: {', '.join(sorted(steps))}")
    print(f"  Total edges: {sum(len(v) for v in graph.values())}\n")

    if detect_negative_cycle(graph):
        print("  ⚠️  Circular dependency with negative cycle detected!\n")
        return

    distances, next_node = johnsons(graph)

    # Show fastest path from Checkout to Deploy
    src, dst = 'Checkout', 'Deploy'
    d = distances.get((src, dst), float('inf'))
    path = reconstruct_path(next_node, src, dst)

    print(f"  ⚡ Fastest path from {src} → {dst}: {d:.0f}s")
    if path:
        print(f"     Path: {' → '.join(path)}\n")

    center, ecc = get_graph_center(graph)
    print(f"  🎯 Most central build step: {center} (max distance to any step: {ecc:.0f}s)")
    print()
    input("  Press Enter to continue...\n")


# ─────────────────────────────────────────────────────────────────────────────
# SCENARIO 3 — Currency Arbitrage Detection (log-transformed exchange rates)
# ─────────────────────────────────────────────────────────────────────────────

def scenario_currency_arbitrage():
    clear_screen()
    print_header("CURRENCY ARBITRAGE DETECTOR  —  Johnson's Algorithm")

    print("SCENARIO:")
    print("  Exchange rates modelled as a directed graph.")
    print("  Edge weight = −log(exchange_rate).")
    print("  A negative cycle = arbitrage opportunity (profit loop).\n")
    separator('-')

    import math

    # Exchange rates (from → to → rate)
    rates = {
        'USD': {'EUR': 0.92,  'GBP': 0.78,  'JPY': 149.5},
        'EUR': {'USD': 1.09,  'GBP': 0.85,  'JPY': 162.4},
        'GBP': {'USD': 1.28,  'EUR': 1.17,  'JPY': 190.5},
        'JPY': {'USD': 0.0067,'EUR': 0.0062,'GBP': 0.0053},
    }

    # Convert to log-weights (negative log = minimise = maximise product)
    graph = {}
    for src, targets in rates.items():
        graph[src] = {}
        for dst, rate in targets.items():
            graph[src][dst] = -math.log(rate)

    currencies = list(graph.keys())
    print(f"  Currencies: {', '.join(currencies)}\n")

    has_neg_cycle = detect_negative_cycle(graph)

    if has_neg_cycle:
        print("  🚨 ARBITRAGE OPPORTUNITY DETECTED!")
        print("     A negative cycle exists — profit loop possible!\n")
    else:
        print("  ✅ No arbitrage opportunity found — market is efficient.\n")

        distances, next_node = johnsons(graph)
        print("  📊 Minimum −log(rate) distance matrix (lower = better exchange):\n")
        display_distance_matrix(distances, currencies)

        print("\n  💡 Best conversion paths:")
        for src in ['USD', 'EUR']:
            for dst in ['JPY', 'GBP']:
                if src != dst:
                    d = distances.get((src, dst), float('inf'))
                    path = reconstruct_path(next_node, src, dst)
                    effective_rate = math.exp(-d) if d != float('inf') else 0
                    route = ' → '.join(path) if path else 'N/A'
                    print(f"    {src} → {dst}: rate ≈ {effective_rate:.4f}  via  {route}")

    print()
    input("  Press Enter to continue...\n")


# ─────────────────────────────────────────────────────────────────────────────
# SCENARIO 4 — Flight Network with Fuel Credits (negative = fuel credit)
# ─────────────────────────────────────────────────────────────────────────────

def scenario_flight_network():
    clear_screen()
    print_header("AIRLINE FUEL COST OPTIMIZER  —  Johnson's Algorithm")

    print("SCENARIO:")
    print("  An airline network where some stopovers earn fuel credits (negative cost).")
    print("  Minimize total fuel cost for all city-pair routes.\n")
    separator('-')

    graph = {
        'LHR': {'CDG': 30,  'DXB': 180, 'JFK': 450},
        'CDG': {'DXB': 140, 'SIN': 420},
        'DXB': {'SIN': -20, 'SYD': 260},    # DXB has fuel credit deal
        'SIN': {'SYD': 80,  'JFK': 350},
        'SYD': {'JFK': 500},
        'JFK': {'LHR': 440, 'CDG': 400},
    }

    airports = set(graph.keys()) | {v for nbrs in graph.values() for v in nbrs}

    print(f"  Airports: {', '.join(sorted(airports))}")
    print(f"  Routes: {sum(len(v) for v in graph.values())}")
    print(f"  Fuel credit route: DXB → SIN  (−$20 credit)\n")

    if detect_negative_cycle(graph):
        print("  ⚠️  Circular fuel credit loop detected — aborted.\n")
        return

    distances, next_node = johnsons(graph)

    print("  📊 All-pairs fuel cost matrix ($):\n")
    display_distance_matrix(distances, airports)

    print("\n  ✈️  Optimal routes:")
    pairs = [('LHR', 'SYD'), ('CDG', 'JFK'), ('LHR', 'SIN')]
    for src, dst in pairs:
        d = distances.get((src, dst), float('inf'))
        path = reconstruct_path(next_node, src, dst)
        route = ' → '.join(path) if path else 'N/A'
        print(f"    {src} → {dst}: ${d:.0f}  via  {route}")

    finite_distances = [d for d in distances.values() if d < float('inf')]
    diameter = max(finite_distances) if finite_distances else float('inf')
    print(f"\n  📏 Network diameter (worst fuel cost): ${diameter:.0f}")
    print()
    input("  Press Enter to continue...\n")


# ─────────────────────────────────────────────────────────────────────────────
# SCENARIO 5 — Manual Graph Builder
# ─────────────────────────────────────────────────────────────────────────────

def scenario_manual_graph():
    clear_screen()
    print_header("MANUAL GRAPH BUILDER  —  Johnson's Algorithm")

    print("  Build your own weighted directed graph and compute all-pairs shortest paths.")
    print("  Supports negative edge weights. Type 'done' when finished.\n")
    separator('-')

    graph = {}

    print("  Enter edges as:  FROM  TO  WEIGHT  (e.g. A B -3)")
    print("  Type 'done' to finish.\n")

    while True:
        entry = input("  Edge: ").strip()
        if entry.lower() == 'done':
            break
        parts = entry.split()
        if len(parts) != 3:
            print("    ⚠️  Format: FROM TO WEIGHT")
            continue
        try:
            u, v, w = parts[0].upper(), parts[1].upper(), float(parts[2])
            graph.setdefault(u, {})[v] = w
            graph.setdefault(v, graph.get(v, {}))   # ensure v exists
            print(f"    ✓ Added {u} → {v}  (w={w})")
        except ValueError:
            print("    ⚠️  Weight must be a number.")

    if not graph:
        print("\n  No graph created. Returning to menu.\n")
        return

    vertices = set(graph.keys()) | {v for nbrs in graph.values() for v in nbrs}
    print(f"\n  Graph has {len(vertices)} vertices, {sum(len(v) for v in graph.values())} edges.\n")

    if detect_negative_cycle(graph):
        print("  🚨 Negative cycle detected — shortest paths are undefined.\n")
    else:
        try:
            distances, next_node = johnsons(graph)
            print("  📊 All-pairs shortest path matrix:\n")
            display_distance_matrix(distances, vertices)

            print("\n  📍 Enter source and destination to see the path (or 'skip'):")
            src = input("    Source: ").strip().upper()
            dst = input("    Dest:   ").strip().upper()
            if src in vertices and dst in vertices:
                d = distances.get((src, dst), float('inf'))
                path = reconstruct_path(next_node, src, dst)
                if path:
                    print(f"\n  ✓ Distance: {d}  Path: {' → '.join(path)}")
                else:
                    print(f"\n  ❌ No path from {src} to {dst}.")
        except ValueError as e:
            print(f"  ⚠️  {e}")

    print()
    input("  Press Enter to continue...\n")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN MENU
# ─────────────────────────────────────────────────────────────────────────────

def main():
    scenarios = {
        '1': ("Intercity Transport Network (subsidised routes)",  scenario_intercity_network),
        '2': ("Software Build Pipeline (caching shortcuts)",      scenario_build_pipeline),
        '3': ("Currency Arbitrage Detector (log-rate model)",     scenario_currency_arbitrage),
        '4': ("Airline Fuel Cost Optimizer (fuel credits)",       scenario_flight_network),
        '5': ("Manual Graph Builder",                             scenario_manual_graph),
        '6': ("Exit", None),
    }

    while True:
        clear_screen()
        print_header("JOHNSON'S ALL-PAIRS SHORTEST PATH  —  Demo App")
        print("  Select a scenario:\n")
        for key, (title, _) in scenarios.items():
            print(f"    {key}. {title}")
        print()

        choice = input("  Option (1-6): ").strip()

        if choice == '6':
            print("\n  Thanks for exploring Johnson's Algorithm!\n")
            break
        elif choice in scenarios:
            _, fn = scenarios[choice]
            fn()
        else:
            print("\n  ⚠️  Invalid choice.\n")
            input("  Press Enter to continue...\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Interrupted. Exiting.\n")
