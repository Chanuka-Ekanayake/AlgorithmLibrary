import sys
import os
import time
from typing import List, Dict, Any

# Add core to path so we can import convex_hull
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.convex_hull import Point, monotone_chain

def run_test_cases() -> int:
    test_cases: List[Dict[str, Any]] = [
        {
            "name": "Square Enclosure",
            "points": [Point(0, 0), Point(10, 0), Point(10, 10), Point(0, 10), Point(5, 5)],
            "expected_count": 4,
            "desc": "Verifies that an interior point (5,5) is correctly excluded."
        },
        {
            "name": "Collinear Points",
            "points": [Point(0, 0), Point(1, 1), Point(2, 2), Point(3, 3)],
            "expected_count": 2,
            "desc": "Checks handling of perfectly linear points (only ends should remain)."
        },
        {
            "name": "Scattered Cloud",
            "points": [Point(0, 3), Point(2, 2), Point(1, 1), Point(2, 1), Point(3, 0), Point(0, 0), Point(3, 3)],
            "expected_count": 4,
            "desc": "A standard cloud of points requiring a counter-clockwise hull."
        }
    ]
    
    print("\n" + "="*65)
    print("  SYSTEM: CONVEX HULL VERIFICATION SUITE")
    print("  ALGORITHM: MONOTONE CHAIN (ANDREW'S)")
    print("="*65 + "\n")
    
    any_failed = False
    start_total = time.perf_counter()

    for i, case in enumerate(test_cases, 1):
        print(f"[{i}] Testing: {case['name']}")
        print(f"    Description: {case['desc']}")
        
        hull = monotone_chain(case["points"])
        
        passed = len(hull) == case["expected_count"]
        status = "PASSED" if passed else "FAILED"
        if not passed:
            any_failed = True
            
        print(f"    Status:      {status}")
        print(f"    Hull Nodes:  {hull}")
        print(f"    Count:       {len(hull)} (Expected: {case['expected_count']})\n")

    elapsed = (time.perf_counter() - start_total) * 1000
    print("="*65)
    print(f"  VERIFICATION COMPLETE in {elapsed:.2f} ms")
    print("="*65)

    if any_failed:
        print("\n  [ERROR] One or more test cases failed. Check implementation logic.")
        return 1
    
    print("\n  [SUCCESS] All geometric constraints satisfied.")
    return 0

if __name__ == "__main__":
    exit_code = run_test_cases()
    sys.exit(exit_code)

