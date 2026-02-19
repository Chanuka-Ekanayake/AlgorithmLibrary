"""
Tarjan's SCC — Real-World Demo Application
Scenario: Microservice Dependency Resolver
===========================================
This app identifies circular dependencies (SCCs) between microservices
in a distributed system. A cycle means services depend on each other
and must be deployed together.
"""

import sys
import os

# Allow running from the test-project directory directly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.tarjans_scc import analyze_graph_connectivity

SEPARATOR = "=" * 60


def print_header(title):
    print(f"\n{SEPARATOR}")
    print(f"  {title}")
    print(SEPARATOR)


def print_sccs(sccs):
    for i, scc in enumerate(sccs, 1):
        marker = "🔁" if len(scc) > 1 else "✅"
        nodes = " ↔ ".join(scc) if len(scc) > 1 else scc[0]
        print(f"  {marker}  SCC {i}: [{nodes}]")


# ─────────────────────────────────────────────
# Scenario 1: Microservice Circular Dependencies
# ─────────────────────────────────────────────
def demo_microservices():
    print_header("MICROSERVICE ARCHITECTURE — Circular Dependency Detector")

    services = [
        "API-Gateway", "Auth-Service", "User-Service",
        "Order-Service", "Payment-Service", "Notification-Service",
        "Inventory-Service", "Analytics-Service"
    ]

    # Directed calls: A → B means A calls B
    calls = [
        ("API-Gateway",       "Auth-Service"),
        ("API-Gateway",       "User-Service"),
        ("Auth-Service",      "User-Service"),
        ("User-Service",      "Order-Service"),
        ("Order-Service",     "Payment-Service"),
        ("Payment-Service",   "Order-Service"),    # ⚠ cycle: Order ↔ Payment
        ("Order-Service",     "Inventory-Service"),
        ("Inventory-Service", "Notification-Service"),
        ("Notification-Service", "Analytics-Service"),
        ("Analytics-Service", "Notification-Service"),  # ⚠ cycle
    ]

    result = analyze_graph_connectivity(services, calls)

    print(f"\n📦 Services: {len(services)}  |  Calls: {len(calls)}")
    print(f"🔍 Strongly Connected? {result['is_strongly_connected']}")
    print(f"\n📊 Strongly Connected Components ({result['num_sccs']} found):\n")
    print_sccs(result["sccs"])

    if result["non_trivial_sccs"]:
        print("\n⚠️  CIRCULAR DEPENDENCIES DETECTED:")
        for scc in result["non_trivial_sccs"]:
            print(f"   → {' ↔ '.join(scc)}")
        print("\n💡 Recommendation: Refactor to break cycles using an event bus or")
        print("   shared library to decouple these services.")
    else:
        print("\n✅ No circular dependencies — clean architecture!")


# ─────────────────────────────────────────────
# Scenario 2: Social Network Influence Groups
# ─────────────────────────────────────────────
def demo_social_network():
    print_header("SOCIAL NETWORK — Mutual Influence Communities")

    users = ["Alice", "Bob", "Charlie", "Dave", "Eve", "Frank"]

    # Directed follows: A → B means A follows B
    follows = [
        ("Alice", "Bob"),
        ("Bob",   "Charlie"),
        ("Charlie", "Alice"),    # ⚠ cycle: Alice ↔ Bob ↔ Charlie
        ("Dave",  "Eve"),
        ("Eve",   "Frank"),
        ("Frank", "Dave"),       # ⚠ cycle: Dave ↔ Eve ↔ Frank
        ("Bob",   "Dave"),       # link between communities
    ]

    result = analyze_graph_connectivity(users, follows)

    print(f"\n👤 Users: {len(users)}  |  Follows: {len(follows)}")
    print(f"\n🏘️  Tightly-Knit Communities (SCCs):\n")
    print_sccs(result["sccs"])
    print("\n💡 These groups mutually follow each other — ideal for targeted")
    print("   community campaigns or group recommendations.")


# ─────────────────────────────────────────────
# Scenario 3: Compiler — Variable Dependency Graph
# ─────────────────────────────────────────────
def demo_compiler():
    print_header("COMPILER ANALYSIS — Detecting Recursive Variable Deps")

    variables = ["main", "init", "loadConfig", "parseArgs",
                 "validateInput", "processData", "writeOutput"]

    # Directed calls between functions
    calls = [
        ("main",          "init"),
        ("main",          "parseArgs"),
        ("init",          "loadConfig"),
        ("loadConfig",    "init"),       # ⚠ cycle: init ↔ loadConfig
        ("parseArgs",     "validateInput"),
        ("validateInput", "processData"),
        ("processData",   "validateInput"),  # ⚠ cycle
        ("processData",   "writeOutput"),
    ]

    result = analyze_graph_connectivity(variables, calls)

    print(f"\n🔧 Functions: {len(variables)}  |  Calls: {len(calls)}")
    print(f"\n🔁 Recursive Groups (SCCs):\n")
    print_sccs(result["sccs"])

    if result["non_trivial_sccs"]:
        print("\n⚠️  RECURSIVE CALL CYCLES DETECTED:")
        for scc in result["non_trivial_sccs"]:
            print(f"   → {' ↔ '.join(scc)}")
        print("\n💡 Recommendation: Introduce memoization or break into a")
        print("   single entry-point with shared state to eliminate recursion.")


# ─────────────────────────────────────────────
# Scenario 4: Fully Strongly Connected Graph
# ─────────────────────────────────────────────
def demo_fully_connected():
    print_header("FULLY CONNECTED DAG — All Nodes Reachable")

    nodes = ["A", "B", "C", "D"]
    edges = [
        ("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"),  # one big cycle
    ]

    result = analyze_graph_connectivity(nodes, edges)
    print(f"\n🔗 Is Strongly Connected: {result['is_strongly_connected']}")
    print(f"   All {len(nodes)} nodes belong to a single SCC.\n")
    print_sccs(result["sccs"])


# ─────────────────────────────────────────────
# Scenario 5: DAG — No SCCs (pure pipeline)
# ─────────────────────────────────────────────
def demo_dag():
    print_header("DATA PIPELINE — Pure DAG (No Cycles)")

    stages = ["Ingest", "Transform", "Validate", "Enrich", "Load"]
    edges = [
        ("Ingest",    "Transform"),
        ("Transform", "Validate"),
        ("Validate",  "Enrich"),
        ("Enrich",    "Load"),
    ]

    result = analyze_graph_connectivity(stages, edges)
    print(f"\n📐 Pipeline Stages: {len(stages)}")
    print(f"🔍 Strongly Connected? {result['is_strongly_connected']}")
    print(f"\n📊 SCCs ({result['num_sccs']} — one per stage in a clean DAG):\n")
    print_sccs(result["sccs"])
    print("\n✅ Clean linear pipeline — safe topological execution order.")


# ─────────────────────────────────────────────
# Runner
# ─────────────────────────────────────────────
if __name__ == "__main__":
    demo_microservices()
    demo_social_network()
    demo_compiler()
    demo_fully_connected()
    demo_dag()
    print(f"\n{SEPARATOR}")
    print("  All scenarios complete.")
    print(SEPARATOR)
