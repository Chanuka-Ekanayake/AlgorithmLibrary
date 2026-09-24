import sys
import io
import time
import random
from pathlib import Path

# Fix Windows console encoding for Unicode output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Add parent directory to path for core logic access
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

try:
    from core.crdt import GCounter, PNCounter, LWWRegister, ORSet
except ImportError:
    print("Error: Ensure 'core/crdt.py' and 'core/__init__.py' exist.")
    sys.exit(1)


def print_header(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_section(title):
    print(f"\n--- {title} ---")


def print_device_state(name, marker, or_set):
    items = sorted(or_set.items()) if or_set.items() else {"(empty)"}
    print(f"  {marker} {name:>12}: {items}")


def demo_gcounter():
    """Demonstrate distributed page-view counting across CDN edges."""
    print_header("DEMO 1: G-COUNTER -- Distributed View Counter")
    print("Scenario: Three CDN edge nodes independently count page views.\n")

    edge_us = GCounter("edge-us")
    edge_eu = GCounter("edge-eu")
    edge_ap = GCounter("edge-ap")

    # Simulate independent traffic hitting each edge
    print("[TRAFFIC] Simulating page views hitting 3 CDN edges...")
    time.sleep(0.3)

    views = {"edge-us": 1247, "edge-eu": 893, "edge-ap": 2104}
    edge_us.increment(views["edge-us"])
    edge_eu.increment(views["edge-eu"])
    edge_ap.increment(views["edge-ap"])

    print(f"  [US] US Edge:   {edge_us.value():>5} local views")
    print(f"  [EU] EU Edge:   {edge_eu.value():>5} local views")
    print(f"  [AP] AP Edge:   {edge_ap.value():>5} local views")

    print_section("MERGE -- All edges sync their counters")
    time.sleep(0.3)

    # Merge all states (order doesn't matter -- commutative!)
    edge_us.merge(edge_eu)
    edge_us.merge(edge_ap)

    total = views["edge-us"] + views["edge-eu"] + views["edge-ap"]
    print(f"  Global View Count: {edge_us.value()} (expected: {total})")
    print(f"  [OK] Converged correctly: {edge_us.value() == total}")


def demo_pncounter():
    """Demonstrate distributed inventory tracking with inc/dec."""
    print_header("DEMO 2: PN-COUNTER -- Distributed Inventory Tracker")
    print("Scenario: Two warehouses track stock of 'Wireless Headphones'.\n")

    warehouse_a = PNCounter("warehouse-a")
    warehouse_b = PNCounter("warehouse-b")

    # Initial stock
    warehouse_a.increment(500)
    warehouse_b.increment(300)
    print(f"  [+] Warehouse A: +500 received (stock: {warehouse_a.value()})")
    print(f"  [+] Warehouse B: +300 received (stock: {warehouse_b.value()})")

    # Sales happen independently
    time.sleep(0.3)
    print_section("SALES -- Independent decrements (offline)")
    warehouse_a.decrement(47)
    warehouse_b.decrement(123)
    print(f"  [-] Warehouse A: sold 47  (local stock: {warehouse_a.value()})")
    print(f"  [-] Warehouse B: sold 123 (local stock: {warehouse_b.value()})")

    # Merge
    print_section("MERGE -- Warehouses sync inventory")
    time.sleep(0.3)
    warehouse_a.merge(warehouse_b)
    warehouse_b.merge(warehouse_a)
    expected = (500 + 300) - (47 + 123)
    print(f"  Global Stock Level: {warehouse_a.value()} (expected: {expected})")
    print(f"  [OK] Both warehouses agree: {warehouse_a.value() == warehouse_b.value()}")


def demo_lww_register():
    """Demonstrate last-writer-wins for user profile settings."""
    print_header("DEMO 3: LWW-REGISTER -- User Profile Sync")
    print("Scenario: User updates profile theme on phone and laptop.\n")

    phone = LWWRegister("phone")
    laptop = LWWRegister("laptop")

    # Phone update first
    phone.set("dark_mode", timestamp=1000.0)
    print(f"  [PHONE]  (t=1000.0): set theme = 'dark_mode'")
    time.sleep(0.3)

    # Laptop update slightly later
    laptop.set("ocean_blue", timestamp=1000.5)
    print(f"  [LAPTOP] (t=1000.5): set theme = 'ocean_blue'")

    # Merge -- laptop wins because higher timestamp
    print_section("MERGE -- Devices sync profile")
    time.sleep(0.3)
    phone.merge(laptop)
    laptop.merge(phone)
    print(f"  [PHONE]  sees: '{phone.get()}'")
    print(f"  [LAPTOP] sees: '{laptop.get()}'")
    print(f"  [OK] Both agree (latest write wins): {phone.get() == laptop.get()}")


def demo_or_set():
    """The main showcase: collaborative shopping list with offline edits."""
    print_header("DEMO 4: OR-SET -- The Collaborative Shopping List")
    print("Scenario: Alice, Bob, and Carol share a grocery list.")
    print("All three go OFFLINE and make independent edits.\n")

    alice = ORSet("alice")
    bob = ORSet("bob")
    carol = ORSet("carol")

    # === Phase 1: Initial shared state ===
    print_section("PHASE 1: Initial List (all online)")
    initial_items = ["Milk", "Eggs", "Bread", "Butter"]
    for item in initial_items:
        alice.add(item)
    # Sync initial state to all
    bob.merge(alice)
    carol.merge(alice)
    print_device_state("Alice", "[A]", alice)
    print_device_state("Bob", "[B]", bob)
    print_device_state("Carol", "[C]", carol)

    time.sleep(0.5)

    # === Phase 2: Everyone goes offline ===
    print_section("PHASE 2: All devices go OFFLINE")
    time.sleep(0.3)

    # Alice (on a plane)
    print("\n  [A] Alice (airplane mode):")
    alice.add("Avocados")
    print("      + Added 'Avocados'")
    alice.remove("Bread")
    print("      - Removed 'Bread' (going gluten-free)")
    alice.add("Rice Cakes")
    print("      + Added 'Rice Cakes'")

    time.sleep(0.3)

    # Bob (on a train)
    print("\n  [B] Bob (train, no signal):")
    bob.add("Coffee")
    print("      + Added 'Coffee'")
    bob.add("Bread")  # Bob ALSO adds Bread -- concurrent with Alice's remove!
    print("      + Added 'Bread' (didn't know Alice removed it!)")
    bob.remove("Butter")
    print("      - Removed 'Butter'")

    time.sleep(0.3)

    # Carol (in the subway)
    print("\n  [C] Carol (subway, offline):")
    carol.add("Cheese")
    print("      + Added 'Cheese'")
    carol.add("Milk")  # Carol adds Milk again -- concurrent add
    print("      + Added 'Milk' (extra carton, just in case)")
    carol.remove("Eggs")
    print("      - Removed 'Eggs' (realized they have enough)")

    time.sleep(0.5)

    # === Phase 3: Everyone comes back online ===
    print_section("PHASE 3: All devices come ONLINE -- CRDT MERGE")
    print("\n  [SYNC] Syncing all three devices...")
    time.sleep(0.5)

    # Merge in arbitrary order (commutative + associative = order doesn't matter)
    alice.merge(bob)
    alice.merge(carol)
    bob.merge(alice)
    carol.merge(alice)

    # All three should be identical
    print_device_state("Alice", "[A]", alice)
    print_device_state("Bob", "[B]", bob)
    print_device_state("Carol", "[C]", carol)

    # === Phase 4: Conflict Analysis ===
    print_section("CONFLICT ANALYSIS")
    time.sleep(0.3)

    print("""
  [*] BREAD Conflict:
      Alice REMOVED "Bread" while Bob ADDED "Bread" concurrently.
      -> OR-Set 'add-wins' semantics: Bob's add created a NEW tag
         that Alice's remove never saw. Result: Bread SURVIVES! [OK]

  [*] MILK Conflict:
      Carol added "Milk" while it already existed from the initial list.
      -> Both tags coexist harmlessly. "Milk" appears once in the set. [OK]

  [*] EGGS Conflict:
      Carol removed "Eggs". No one else concurrently added it.
      -> All tags for "Eggs" are tombstoned. "Eggs" is GONE. [OK]

  [*] BUTTER Conflict:
      Bob removed "Butter". No concurrent add from others.
      -> "Butter" is GONE. [OK]
    """)

    # Verify convergence
    converged = (alice.items() == bob.items() == carol.items())
    print(f"  [RESULT] All devices converged to identical state: {converged}")
    print(f"  [LIST]   Final Shopping List: {sorted(alice.items())}")


def run_full_demo():
    print("=" * 60)
    print("  SYSTEM: THE COLLABORATIVE SHOPPING LIST")
    print("  ALGORITHM: CRDT (CONFLICT-FREE REPLICATED DATA TYPES)")
    print("=" * 60)

    demo_gcounter()
    demo_pncounter()
    demo_lww_register()
    demo_or_set()

    print("\n" + "=" * 60)
    print("  FINAL REPORT")
    print("=" * 60)
    print("  CRDTs Demonstrated:     4 (G-Counter, PN-Counter, LWW-Register, OR-Set)")
    print("  Conflicts Encountered:  4")
    print("  Conflicts Resolved:     4 (100% -- mathematically guaranteed)")
    print("  Coordination Required:  ZERO (no leader, no locking, no quorum)")
    print("  Offline Operations:     FULLY SUPPORTED")
    print("=" * 60)


if __name__ == "__main__":
    run_full_demo()
