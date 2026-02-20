"""
Hierholzer's Algorithm — Real-World Demo Application
Scenario: Delivery Route Planner + 4 Other Use Cases
=====================================================
Finds a route that covers every road/connection exactly once.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.hierholzers import HierholzersEulerian, plan_route

SEPARATOR = "=" * 62


def print_header(title):
    print(f"\n{SEPARATOR}")
    print(f"  {title}")
    print(SEPARATOR)


def print_route(route, label="Route"):
    print(f"\n  📍 {label}:")
    print("     " + " → ".join(str(v) for v in route))


# ─────────────────────────────────────────────
# Scenario 1: Delivery Van Route Optimizer
# ─────────────────────────────────────────────
def demo_delivery_route():
    print_header("DELIVERY VAN — Cover Every Street Exactly Once")

    locations = ["Depot", "Zone-A", "Zone-B", "Zone-C", "Zone-D", "Zone-E"]
    roads = [
        ("Depot",  "Zone-A"),
        ("Zone-A", "Zone-B"),
        ("Zone-B", "Zone-C"),
        ("Zone-C", "Zone-A"),   # loop
        ("Zone-C", "Zone-D"),
        ("Zone-D", "Zone-E"),
        ("Zone-E", "Zone-B"),
        ("Zone-B", "Depot"),
    ]

    result = plan_route(locations, roads, directed=True)

    print(f"\n  📦 Locations : {len(locations)}")
    print(f"  🛣️  Roads     : {len(roads)}")
    print(f"  🔍 Feasible  : {result['feasible']}")
    print(f"  📝 Type      : {result['type'].capitalize()}")
    print_route(result["route"], "Optimal Delivery Route")
    print(f"\n  💡 {result['summary']}")


# ─────────────────────────────────────────────
# Scenario 2: Königsberg Bridge Problem (Historic)
# ─────────────────────────────────────────────
def demo_konigsberg():
    print_header("KÖNIGSBERG BRIDGE PROBLEM — Euler's Original (1736)")

    # 4 landmasses: North, South, East, Island
    # 7 bridges connecting them (undirected)
    g = HierholzersEulerian(directed=False)
    bridges = [
        ("North",  "Island"),
        ("North",  "Island"),   # two bridges between North and Island
        ("South",  "Island"),
        ("South",  "Island"),   # two bridges between South and Island
        ("East",   "Island"),
        ("North",  "East"),
        ("South",  "East"),
    ]
    for u, v in bridges:
        g.add_edge(u, v)

    info = g.get_path_info()
    print(f"\n  🏛️  Landmasses : North, South, East, Island")
    print(f"  🌉 Bridges    : {len(bridges)}")
    print(f"\n  Has Eulerian Circuit : {info['has_circuit']}")
    print(f"  Has Eulerian Path    : {info['has_path']}")

    if not info["has_path"] and not info["has_circuit"]:
        print("\n  ❌ RESULT: It is IMPOSSIBLE to cross every bridge exactly once.")
        print("     Euler proved this in 1736 — the birth of Graph Theory! 🎓")
    else:
        print_route(info["path"])


# ─────────────────────────────────────────────
# Scenario 3: Network Cable Inspection
# ─────────────────────────────────────────────
def demo_network_inspection():
    print_header("NETWORK CABLE INSPECTION — Visit Every Link Once")

    # Undirected network — technician must inspect every cable
    cables = [
        ("Server", "Switch1"),
        ("Switch1", "Switch2"),
        ("Switch2", "Firewall"),
        ("Firewall", "Router"),
        ("Router", "Switch1"),
        ("Switch2", "Router"),
    ]
    locations = list({n for edge in cables for n in edge})

    result = plan_route(locations, cables, directed=False)

    print(f"\n  🖥️  Nodes   : {len(locations)}")
    print(f"  🔌 Cables  : {len(cables)}")
    print(f"  🔍 Feasible: {result['feasible']}")
    print_route(result["route"], "Inspection Route")
    print(f"\n  💡 {result['summary']}")


# ─────────────────────────────────────────────
# Scenario 4: DNA Sequence Assembly (De Bruijn Graph)
# ─────────────────────────────────────────────
def demo_dna_assembly():
    print_header("DNA ASSEMBLY — Reconstruct Sequence from Fragments")

    # DNA k-mers as directed edges: each edge = one k-mer overlap
    # Eulerian path through De Bruijn graph reconstructs the sequence
    g = HierholzersEulerian(directed=True)
    # k=3 fragments from sequence "ATGCATG"
    kmers = [("ATG", "TGC"), ("TGC", "GCA"), ("GCA", "CAT"),
             ("CAT", "ATG"), ("ATG", "TGG")]  # add one branch
    for u, v in kmers:
        g.add_edge(u, v)

    info = g.get_path_info()
    print(f"\n  🧬 k-mers (fragments): {len(kmers)}")
    print(f"  Has Eulerian Path   : {info['has_path']}")
    if info["path"]:
        sequence = info["path"][0] + "".join(node[-1] for node in info["path"][1:])
        print_route(info["path"], "De Bruijn Traversal")
        print(f"\n  🔬 Reconstructed DNA: {sequence}")
    else:
        print("\n  ❌ Cannot reconstruct — fragments do not form valid Eulerian path.")


# ─────────────────────────────────────────────
# Scenario 5: Pen-Drawing Puzzle (One Stroke)
# ─────────────────────────────────────────────
def demo_one_stroke():
    print_header("ONE-STROKE DRAWING — Can You Draw Without Lifting the Pen?")

    # Simple shape: a house outline
    # Undirected edges
    g = HierholzersEulerian(directed=False)
    strokes = [
        ("BottomLeft", "BottomRight"),
        ("BottomRight", "TopRight"),
        ("TopRight", "TopLeft"),
        ("TopLeft", "BottomLeft"),   # square base
        ("TopLeft", "Peak"),
        ("Peak", "TopRight"),        # roof
    ]
    for u, v in strokes:
        g.add_edge(u, v)

    info = g.get_path_info()
    print(f"\n  ✏️  Edges (strokes): {len(strokes)}")
    print(f"  Has Eulerian Path   : {info['has_path']}")
    print(f"  Has Eulerian Circuit: {info['has_circuit']}")

    if info["path"]:
        print_route(info["path"], "One-stroke path")
        if info["type"] == "circuit":
            print("\n  ✅ Can draw AND return to start — perfect closed shape!")
        else:
            print(f"\n  ✅ Can draw in one stroke: {info['path'][0]} → {info['path'][-1]}")
    else:
        print("\n  ❌ Cannot draw this shape without lifting the pen.")


# ─────────────────────────────────────────────
# Runner
# ─────────────────────────────────────────────
if __name__ == "__main__":
    demo_delivery_route()
    demo_konigsberg()
    demo_network_inspection()
    demo_dna_assembly()
    demo_one_stroke()
    print(f"\n{SEPARATOR}")
    print("  All scenarios complete.")
    print(SEPARATOR)
