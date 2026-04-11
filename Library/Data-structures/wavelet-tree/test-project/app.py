import sys
import os
import random

# Allow importing from the core/ directory two levels up
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.wavelet_tree import WaveletTree


# ---------------------------------------------------------------------------
# ANSI colour helpers (Windows 10+ and all Unix terminals)
# ---------------------------------------------------------------------------
GREEN  = "\033[92m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"


def header(text: str) -> None:
    print(f"\n{BOLD}{CYAN}{'=' * 62}{RESET}")
    print(f"{BOLD}{CYAN}  {text}{RESET}")
    print(f"{BOLD}{CYAN}{'=' * 62}{RESET}")


def section(text: str) -> None:
    print(f"\n{YELLOW}--- {text} ---{RESET}")


def ok(text: str) -> None:
    print(f"  {GREEN}[OK] {text}{RESET}")


# ---------------------------------------------------------------------------
# Scenario 1 — IoT Sensor Analytics
# ---------------------------------------------------------------------------

def run_sensor_scenario() -> None:
    """
    SCENARIO 1 - IoT Sensor Analytics
    A factory floor has 12 temperature sensors. Each sensor records a
    temperature reading (in C) at the same timestamp. Operations needed:

      - What is the MEDIAN temperature across sensors 2-9?
      - How many sensors in range 0-7 are reading BELOW the alert threshold?
      - How often is the EXACT critical value 85C appearing in range 3-11?

    All answered without sorting, in O(log V) per query.
    """
    header("SCENARIO 1 : IoT Sensor Analytics")

    readings = [72, 58, 85, 91, 63, 85, 77, 68, 85, 54, 90, 61]
    wt = WaveletTree(readings)

    print(f"\n  Sensor readings (sensor 0 to 11):")
    print(f"  {readings}")

    section("Median temperature - sensors 2 to 9")
    median = wt.range_median(2, 9)
    ok(f"Median of sensors 2-9  = {median}C")
    sorted_slice = sorted(readings[2:10])
    naive_median = sorted_slice[len(sorted_slice) // 2 - (1 - len(sorted_slice) % 2)]
    ok(f"Verified (sorted slice) = {sorted_slice}  -> median = {naive_median}C")

    section("Alert check - how many sensors in range 0-7 read below 75C?")
    alert_threshold = 75
    below = wt.count_less_than(0, 7, alert_threshold)
    naive_below = sum(1 for v in readings[0:8] if v < alert_threshold)
    ok(f"Sensors 0-7 below {alert_threshold}C = {below}")
    ok(f"Expected (naive)        = {naive_below}  ({'Match' if below == naive_below else 'MISMATCH'})")

    section("Critical value frequency - how many times does 85C appear in sensors 3-11?")
    freq = wt.range_frequency(3, 11, 85)
    naive_freq = readings[3:12].count(85)
    ok(f"Frequency of 85C (3-11) = {freq}")
    ok(f"Expected (naive)         = {naive_freq}  ({'Match' if freq == naive_freq else 'MISMATCH'})")


# ---------------------------------------------------------------------------
# Scenario 2 — E-Commerce Order Analytics
# ---------------------------------------------------------------------------

def run_database_scenario() -> None:
    """
    SCENARIO 2 - E-Commerce Order Analytics
    A database holds order totals (in $) for 15 recent transactions stored in
    order-of-arrival (not sorted). A reporting engine must answer:

      - What is the 3rd smallest order value in transactions 5-14?
      - How many orders in transactions 2-14 were under $500?
      - How many transactions (0-14) had EXACTLY $320?
    """
    header("SCENARIO 2 : E-Commerce Order Analytics")

    orders = [250, 780, 120, 320, 640, 480, 320, 910, 55, 320, 700, 430, 180, 560, 990]
    wt = WaveletTree(orders)

    print(f"\n  Order amounts (transaction 0 to 14):")
    print(f"  {orders}")

    section("3rd smallest order - last 10 transactions (indices 5-14)")
    k3 = wt.kth_smallest(5, 14, 3)
    sorted_last10 = sorted(orders[5:15])
    ok(f"3rd smallest in txns 5-14  = ${k3}")
    ok(f"Verified (sorted)           = {sorted_last10}  -> 3rd = ${sorted_last10[2]}")

    section("Count orders under $500 - transactions 2 to 14")
    count_under = wt.count_less_than(2, 14, 500)
    naive_count_under = sum(1 for v in orders[2:15] if v < 500)
    ok(f"Orders < $500 in txns 2-14  = {count_under}")
    ok(f"Expected (naive)             = {naive_count_under}  ({'Match' if count_under == naive_count_under else 'MISMATCH'})")

    section("Frequency of $320 orders - full dataset (0-14)")
    freq_320 = wt.range_frequency(0, 14, 320)
    naive_freq_320 = orders.count(320)
    ok(f"Occurrences of $320         = {freq_320}")
    ok(f"Expected (naive)             = {naive_freq_320}  ({'Match' if freq_320 == naive_freq_320 else 'MISMATCH'})")


# ---------------------------------------------------------------------------
# Scenario 3 — Range Order Statistics (Competitive Style)
# ---------------------------------------------------------------------------

def run_competitive_scenario() -> None:
    """
    SCENARIO 3 - Range Order Statistics (Competitive Style)
    Given a static array, answer a batch of mixed order-statistic queries.
    Demonstrates the Wavelet Tree handling values with wide spread and
    multiple distinct queries on the same structure.
    """
    header("SCENARIO 3 : Range Order Statistics")

    arr = [4, 2, 7, 1, 9, 3, 6, 8, 5, 2, 7, 4, 1, 6, 3]
    wt = WaveletTree(arr)

    print(f"\n  Array (indices 0 to 14):")
    print(f"  {arr}")

    queries = [
        ("kth_smallest",    0, 14, 1,    "Minimum of entire array"),
        ("kth_smallest",    0, 14, 15,   "Maximum of entire array"),
        ("kth_smallest",    2,  8, 4,    "4th smallest in indices 2-8"),
        ("count_less_than", 0, 14, 5,    "Count < 5 in full array"),
        ("range_frequency", 0, 14, 7,    "Frequency of 7 in full array"),
        ("range_median",    0, 14, None, "Median of entire array"),
    ]

    section("Batch Queries")
    for q in queries:
        op = q[0]
        l, r = q[1], q[2]
        result_label = q[4]

        if op == "kth_smallest":
            k = q[3]
            result = wt.kth_smallest(l, r, k)
            naive = sorted(arr[l:r+1])[k-1]
            match = "OK" if result == naive else "MISMATCH"
            ok(f"{result_label:42s} -> {result}  (naive={naive}) [{match}]")

        elif op == "count_less_than":
            x = q[3]
            result = wt.count_less_than(l, r, x)
            naive = sum(1 for v in arr[l:r+1] if v < x)
            match = "OK" if result == naive else "MISMATCH"
            ok(f"{result_label:42s} -> {result}  (naive={naive}) [{match}]")

        elif op == "range_frequency":
            x = q[3]
            result = wt.range_frequency(l, r, x)
            naive = arr[l:r+1].count(x)
            match = "OK" if result == naive else "MISMATCH"
            ok(f"{result_label:42s} -> {result}  (naive={naive}) [{match}]")

        elif op == "range_median":
            result = wt.range_median(l, r)
            s = sorted(arr[l:r+1])
            naive = s[(len(s)+1)//2 - 1]
            match = "OK" if result == naive else "MISMATCH"
            ok(f"{result_label:42s} -> {result}  (naive={naive}) [{match}]")


# ---------------------------------------------------------------------------
# Stress Test
# ---------------------------------------------------------------------------

def run_stress_test() -> None:
    """
    STRESS TEST - verifies all three query types against naive O(n) brute-force.
    Runs 300 random queries on a random array of 200 elements.
    """
    header("STRESS TEST : Wavelet Tree vs Naive Brute-Force")

    n = 200
    arr = [random.randint(1, 50) for _ in range(n)]
    wt = WaveletTree(arr)

    errors = 0
    trials = 300

    for _ in range(trials):
        l = random.randint(0, n - 1)
        r = random.randint(l, n - 1)
        op = random.choice(["kth", "count_lt", "freq"])

        sub = arr[l:r+1]

        if op == "kth":
            k = random.randint(1, r - l + 1)
            got = wt.kth_smallest(l, r, k)
            expected = sorted(sub)[k - 1]
            if got != expected:
                errors += 1
                print(f"  MISMATCH kth_smallest({l},{r},{k}): got {got}, expected {expected}")

        elif op == "count_lt":
            x = random.randint(0, 55)
            got = wt.count_less_than(l, r, x)
            expected = sum(1 for v in sub if v < x)
            if got != expected:
                errors += 1
                print(f"  MISMATCH count_less_than({l},{r},{x}): got {got}, expected {expected}")

        elif op == "freq":
            x = random.randint(1, 50)
            got = wt.range_frequency(l, r, x)
            expected = sub.count(x)
            if got != expected:
                errors += 1
                print(f"  MISMATCH range_frequency({l},{r},{x}): got {got}, expected {expected}")

    if errors == 0:
        ok(f"All {trials} random queries passed!")
    else:
        print(f"  {errors} mismatches out of {trials} - BUG DETECTED!")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    print(f"\n{BOLD}WAVELET TREE - DEMO{RESET}")
    print("Range order-statistics queries answered in O(log V) per query\n")

    run_sensor_scenario()
    run_database_scenario()
    run_competitive_scenario()
    run_stress_test()

    print(f"\n{BOLD}{GREEN}All scenarios complete!{RESET}\n")


if __name__ == "__main__":
    main()
