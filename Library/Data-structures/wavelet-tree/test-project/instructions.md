# Running the Wavelet Tree Simulation

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

The simulation walks through **3 real-world scenarios**, each demonstrating a different power of the Wavelet Tree:

| Scenario | Description |
|---|---|
| **1. IoT Sensor Analytics** | Find the median sensor reading, count readings below an alert threshold, and measure critical-value frequency — all in O(log V). |
| **2. E-Commerce Order Analytics** | Answer order-statistics questions on raw (unsorted) transaction data: k-th smallest amount, count under a price limit, frequency of a specific amount. |
| **3. Range Order Statistics** | A batch of mixed queries on a static integer array — minimum, maximum, k-th smallest, count less than, frequency, and median. |

After the scenarios, a **stress test** runs 300 random queries comparing Wavelet Tree output against brute-force array operations — confirming 100% correctness.

## Expected Output (Sample)

```
WAVELET TREE — DEMO

==============================================================
  SCENARIO 1 : IoT Sensor Analytics
==============================================================

  Sensor readings (sensor 0 → 11):
  [72, 58, 85, 91, 63, 85, 77, 68, 85, 54, 90, 61]

--- Median temperature — sensors 2 to 9 ---
  ✔  Median of sensors 2–9  = 77°C
  ...

--- STRESS TEST ---
  ✔  All 300 random queries passed! ✓

All scenarios complete!
```
