# Running the Segment Tree Simulation

## Prerequisites

- Python 3.8 or higher (no external dependencies required)

## Steps

### 1. Navigate to the test-project directory

```bash
cd test-project
```

### 2. Run the application

```bash
python app.py
```

## What to Expect

The simulation walks through **3 real-world scenarios**, each demonstrating a different power of the Segment Tree with Lazy Propagation:

| Scenario | Description |
|---|---|
| **1. Stock Volume Tracker** | Range sum queries + bulk volume corrections over a 10-day trading window. |
| **2. Game Leaderboard** | Apply a score boost event to a range of players and re-query totals. |
| **3. E-commerce Price Engine** | Apply a flash-sale discount and a restock fee independently across different product ranges. |

After the scenarios, a **stress test** runs 200 random operations comparing the Segment Tree output against a naive brute-force array — confirming 100% correctness.

## Expected Output (Sample)

```
SEGMENT TREE WITH LAZY PROPAGATION — DEMO

==========================================================
  SCENARIO 1 : Stock Volume Tracker
==========================================================

  Initial daily volumes (day 0–9):
  Volumes: [120, 95, 210, 180, 300, 75, 440, 260, 150, 330]

--- Range Query — total volume days 2 to 6 ---
  ✔ Total volume days 2–6 = 1205k shares
  ✔ Expected             = 1205k shares  (✓ Match)
...
  ✔ All 200 random operations passed! ✓

All scenarios complete!
```
