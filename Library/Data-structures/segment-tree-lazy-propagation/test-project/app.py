import sys
import os

# Allow importing from the parent directory (core/)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.segment_tree import SegmentTree


# ---------------------------------------------------------------------------
# ANSI colour helpers (work on Windows 10+ and all Unix terminals)
# ---------------------------------------------------------------------------
GREEN  = "\033[92m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

def header(text: str) -> None:
    print(f"\n{BOLD}{CYAN}{'=' * 58}{RESET}")
    print(f"{BOLD}{CYAN}  {text}{RESET}")
    print(f"{BOLD}{CYAN}{'=' * 58}{RESET}")

def section(text: str) -> None:
    print(f"\n{YELLOW}--- {text} ---{RESET}")

def ok(text: str) -> None:
    print(f"  {GREEN}✔ {text}{RESET}")


# ---------------------------------------------------------------------------
# Scenario helpers
# ---------------------------------------------------------------------------

def print_array(label: str, st: SegmentTree) -> None:
    """Reconstruct and print the current state of the underlying array."""
    values = [st.point_query(i) for i in range(st.n)]
    print(f"  {label}: {values}")


def run_stock_scenario() -> None:
    """
    SCENARIO 1 — Stock Volume Tracker
    ─────────────────────────────────
    A brokerage tracks daily traded volumes (in thousands of shares) for
    a stock over 10 days. Operations:
      • Query total volume traded between two dates.
      • Apply a bulk correction (add/subtract) to a range of days.
    """
    header("SCENARIO 1 : Stock Volume Tracker")

    # Daily volumes (Day 0 → Day 9)
    daily_volumes = [120, 95, 210, 180, 300, 75, 440, 260, 150, 330]
    st = SegmentTree(daily_volumes)

    print(f"\n  Initial daily volumes (day 0–9):")
    print_array("  Volumes", st)

    section("Range Query — total volume days 2 to 6")
    total = st.query(2, 6)
    ok(f"Total volume days 2–6 = {total}k shares")
    expected = sum(daily_volumes[2:7])
    ok(f"Expected             = {expected}k shares  ({'✓ Match' if total == expected else '✗ MISMATCH'})")

    section("Bulk Correction — reporting error on days 3–5 (+50k each)")
    st.update(3, 5, 50)
    print_array("  Updated volumes", st)
    new_total = st.query(2, 6)
    ok(f"New total volume days 2–6 = {new_total}k shares")

    section("Point Query — single day (day 4)")
    ok(f"Volume on day 4 = {st.point_query(4)}k shares")


def run_game_leaderboard_scenario() -> None:
    """
    SCENARIO 2 — Game Leaderboard Score Boost
    ─────────────────────────────────────────
    During a weekend event, all players ranked 3rd to 7th receive a
    +500 bonus score. The system must quickly answer range score queries.
    """
    header("SCENARIO 2 : Game Leaderboard Score Boost")

    player_scores = [8200, 7400, 6900, 6300, 5800, 5100, 4700, 4200, 3500, 3000]
    st = SegmentTree(player_scores)

    print(f"\n  Player scores (rank 0 = top):")
    print_array("  Scores", st)

    section("Query — total score of top 5 players (ranks 0–4)")
    top5 = st.query(0, 4)
    ok(f"Top-5 combined score = {top5}")

    section("Weekend event: +500 bonus for ranks 2–6")
    st.update(2, 6, 500)
    print_array("  Scores after bonus", st)

    section("Re-query — combined score of ranks 2–6 after boost")
    mid_total = st.query(2, 6)
    ok(f"Ranks 2–6 combined score = {mid_total}")

    section("Point Query — score of rank #3 (0-indexed)")
    ok(f"Score of rank-3 player = {st.point_query(3)}")


def run_database_range_update_scenario() -> None:
    """
    SCENARIO 3 — E-commerce Price Range Update
    ────────────────────────────────────────────
    An e-commerce engine has 8 product prices. A flash-sale applies
    a flat discount to products 1–5, then a restock fee to products 4–7.
    """
    header("SCENARIO 3 : E-commerce Flash-Sale Price Engine")

    prices = [999, 1499, 2499, 3999, 1299, 799, 4999, 2199]
    st = SegmentTree(prices)

    print(f"\n  Product prices (IDs 0–7):")
    print_array("  Prices", st)

    section("Flash sale: -200 discount on products 1 to 5")
    st.update(1, 5, -200)
    print_array("  After discount", st)

    section("Restock fee: +100 on products 4 to 7")
    st.update(4, 7, 100)
    print_array("  After restock fee", st)

    section("Query — total revenue if all products are sold")
    total_revenue = st.query(0, 7)
    ok(f"Total projected revenue = ₹{total_revenue}")

    section("Query — revenue for mid-range products (IDs 2–5)")
    mid_revenue = st.query(2, 5)
    ok(f"Mid-range revenue = ₹{mid_revenue}")


def run_stress_test() -> None:
    """
    STRESS TEST — verifies correctness against a naive O(n) reference.
    """
    import random
    header("STRESS TEST : Segment Tree vs Naive Array")

    n = 100
    data = [random.randint(1, 100) for _ in range(n)]
    naive = data[:]
    st = SegmentTree(data)

    errors = 0
    trials = 200

    for _ in range(trials):
        op = random.choice(["update", "query"])
        l = random.randint(0, n - 1)
        r = random.randint(l, n - 1)

        if op == "update":
            val = random.randint(-20, 20)
            st.update(l, r, val)
            for i in range(l, r + 1):
                naive[i] += val
        else:
            seg_ans = st.query(l, r)
            naive_ans = sum(naive[l:r + 1])
            if seg_ans != naive_ans:
                errors += 1
                print(f"  MISMATCH: query({l},{r}) → ST={seg_ans}, Naive={naive_ans}")

    if errors == 0:
        ok(f"All {trials} random operations passed! ✓")
    else:
        print(f"  {errors} mismatches found out of {trials} trials — BUG DETECTED!")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    print(f"\n{BOLD}SEGMENT TREE WITH LAZY PROPAGATION — DEMO{RESET}")
    print("Real-world scenarios demonstrating O(log n) range operations\n")

    run_stock_scenario()
    run_game_leaderboard_scenario()
    run_database_range_update_scenario()
    run_stress_test()

    print(f"\n{BOLD}{GREEN}All scenarios complete!{RESET}\n")


if __name__ == "__main__":
    main()
