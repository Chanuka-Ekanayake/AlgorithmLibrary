# Kruskal's MST Edge Sorter - Test Project Instructions

## Overview

Interactive demonstration of Kruskal's Minimum Spanning Tree algorithm using edge-based sorting and Union-Find for cycle detection.

## Quick Start

```bash
cd test-project
python app.py
```

## Algorithm Approach

**Kruskal's Strategy:** Sort all edges by weight, then greedily add cheapest edges that don't create cycles.

**Key Difference from Prim's:** Processes edges globally (not from a starting vertex).

## Features

### 1. Sample Network
Pre-loaded telecommunications network:
- 9 data centers (DC1-DC9)
- 18 possible fiber connections
- Realistic installation costs

### 2. Custom Network Builder
Create your own network:
```
Connection: CityA CityB 100
✅ Added: CityA ↔ CityB ($100K)

Connection: CityB CityC 80
✅ Added: CityB ↔ CityC ($80K)

Connection: done
```

### 3. Edge Visualization
View all edges sorted by cost:
```
📋 ALL EDGES (Sorted by Cost):
1. DC7 ━━ $  1.00K ━━ DC8
2. DC3 ━━ $  2.00K ━━ DC9
3. DC6 ━━ $  2.00K ━━ DC7
4. DC1 ━━ $  4.00K ━━ DC2
...
```

### 4. Step-by-Step Construction
Watch Kruskal's algorithm work:
```
--- Step 1: Consider edge DC7 ━━ DC8 ($1K) ---
   ✅ Add to MST!
      DC7 component: DC7
      DC8 component: DC8
      → Unite components
      MST edges so far: 1
      Total cost: $1.00K

--- Step 2: Consider edge DC3 ━━ DC9 ($2K) ---
   ✅ Add to MST!
   ...

--- Step 8: Consider edge DC2 ━━ DC8 ($11K) ---
   ❌ Skip: DC2 and DC8 already in same component
      (would create cycle)
```

### 5. Direct MST Calculation
Fast calculation without step details:
```
✅ Minimum Spanning Tree Found!
   Total Cost: $37.00K
   Edges Used: 8 of 18
   💰 Savings: $38.00K (50.7%)

📊 EDGE STATISTICS:
   Cheapest Edge: $1.00K
   Most Expensive: $8.00K
   Average Cost: $4.62K
```

### 6. Critical Edge Analysis
Identify most important connections:
```
⚠️  All MST edges are critical!
   Removing ANY edge disconnects the network.

💸 Most Expensive Critical Edges:
   1. DC1 ↔ DC8: $8.00K
   2. DC3 ↔ DC4: $7.00K
   ...
```

### 7. Algorithm Comparison
Compare Kruskal's with Prim's:
```
Aspect           | Kruskal's          | Prim's
-----------------|--------------------|-----------------
Approach         | Global edge sort   | Local growth
Data Structure   | Union-Find         | Priority Queue
Time Complexity  | O(E log E)         | O(E log V)
Best For         | Sparse graphs      | Dense graphs
```

## Usage Examples

### Example 1: Sample Network

```
Select option: 1
✅ Sample network loaded!

📊 NETWORK INFORMATION
Data Centers:        9
Possible Connections: 18
Total Cost (all):    $75.00K
Network Density:     50.0%

Select option: 6

🔧 Calculating MST using Kruskal's algorithm...

✅ Minimum Spanning Tree Found!
   Total Cost: $37.00K
   Edges Used: 8 of 18
   💰 Savings: $38.00K (50.7%)

🌳 MST EDGES (by weight):
   DC7      ━━━ $  1.00K ━━━ DC8
   DC3      ━━━ $  2.00K ━━━ DC9
   DC6      ━━━ $  2.00K ━━━ DC7
   DC1      ━━━ $  4.00K ━━━ DC2
   DC3      ━━━ $  4.00K ━━━ DC6
   DC3      ━━━ $  7.00K ━━━ DC4
   DC1      ━━━ $  8.00K ━━━ DC8
   DC4      ━━━ $  9.00K ━━━ DC5
```

### Example 2: Custom Small Network

```
Select option: 2

--- Custom Network Builder ---
Connection: A B 5
✅ Added: A ↔ B ($5K)

Connection: B C 3
✅ Added: B ↔ C ($3K)

Connection: A C 7
✅ Added: A ↔ C ($7K)

Connection: C D 2
✅ Added: C ↔ D ($2K)

Connection: done

Select option: 5

🔧 KRUSKAL'S ALGORITHM - STEP BY STEP

📌 Initial: 4 separate components
   Components: {A}, {B}, {C}, {D}

--- Step 1: Consider edge C ━━ D ($2K) ---
   ✅ Add to MST!
      C component: C
      D component: D
      → Unite components
      MST edges so far: 1
      Total cost: $2.00K

--- Step 2: Consider edge B ━━ C ($3K) ---
   ✅ Add to MST!
      B component: B
      C component: C
      → Unite components
      MST edges so far: 2
      Total cost: $5.00K

--- Step 3: Consider edge A ━━ B ($5K) ---
   ✅ Add to MST!
      A component: A
      B component: B
      → Unite components
      MST edges so far: 3
      Total cost: $10.00K

🎉 MST COMPLETE! All 4 nodes connected.

Result: MST cost = $10K
Edges: C-D ($2), B-C ($3), A-B ($5)
Saved: $7K by not using A-C ($7)
```

## Understanding the Output

### Union-Find Cycle Detection

**Why skip edge?**
```
--- Step 8: Consider edge DC2 ━━ DC8 ($11K) ---
   ❌ Skip: DC2 and DC8 already in same component
      (would create cycle)
```

**Explanation:**
- DC2 and DC8 are already connected through other edges
- Adding DC2-DC8 would create a cycle
- Union-Find detects this in nearly O(1) time!

### Cost Savings

```
💰 Savings: $38.00K (50.7%)
```

**Meaning:**
- Building all 18 connections would cost $75K
- MST only needs 8 connections for $37K
- Saves $38K (50.7% reduction)

### Edge Statistics

```
Cheapest Edge: $1.00K
Most Expensive: $8.00K
Average Cost: $4.62K
```

**Insight:** MST prioritizes cheap edges first (greedy approach).

## Real-World Scenarios

### Scenario 1: Telecommunications Network

**Problem:** Connect data centers with minimum fiber cost.

**Graph characteristics:**
- Medium density (50%)
- Wide range of costs
- All centers must connect

**Kruskal's Advantage:**
- Globally optimal edge selection
- Simple to verify correctness
- Natural handling of cost priorities

### Scenario 2: Circuit Board Layout

**Problem:** Connect components with minimum trace length.

**Graph characteristics:**
- Very sparse (few viable connections)
- Many components
- Length = cost

**Kruskal's Advantage:**
- Excellent for sparse graphs
- O(E log E) very efficient when E << V²
- Edge-centric view matches problem

### Scenario 3: Road Network Planning

**Problem:** Connect cities with minimum construction cost.

**Graph characteristics:**
- Sparse to medium density
- Widely varying terrain costs
- May have disconnected regions

**Kruskal's Advantage:**
- Handles disconnected graphs (creates forest)
- Cost-aware (terrain differences)
- Intuitive edge-by-edge approach

## Algorithm Performance

### Time Complexity

**Operations:**
1. Extract edges: O(E)
2. **Sort edges: O(E log E)** ← Dominates!
3. Union-Find init: O(V)
4. Process edges: O(E × α(V)) ≈ O(E)

**Total: O(E log E)**

### Space Complexity

- Edge list: O(E)
- Union-Find: O(V)
- MST output: O(V)

**Total: O(V + E)**

### Practical Performance

| Nodes | Edges | Time |
|-------|-------|------|
| 100 | 500 | < 5 ms |
| 1,000 | 5,000 | < 50 ms |
| 10,000 | 50,000 | < 800 ms |

## Union-Find Optimizations

### Path Compression

```
Before find(E):
A → B → C → D → E

After find(E):
A → E
B → E
C → E
D → E
(All point to root directly)
```

**Benefit:** Future finds are O(1)!

### Union by Rank

```
Attach smaller tree under larger:

Small (rank 1)    Large (rank 3)
      •                 •
                       /|\
                      • • •

Result: Combined tree keeps rank 3
```

**Benefit:** Trees stay shallow (logarithmic height).

**Combined effect:** O(α(V)) ≈ O(1) for practical purposes!

## Common Questions

### Q: Why is edge sorted first?

**A:** Greedy strategy requires processing cheapest edges first to guarantee minimum total cost.

### Q: What if multiple edges have same weight?

**A:** Multiple valid MSTs may exist. All have the same total cost. Kruskal's finds one of them.

### Q: How does it detect cycles?

**A:** Union-Find tracks which component each vertex belongs to. If both endpoints of an edge are in the same component, adding the edge would create a cycle.

### Q: Can it handle disconnected graphs?

**A:** Yes! It naturally finds a Minimum Spanning Forest (MST for each component).

### Q: When is Kruskal's better than Prim's?

**A:** Sparse graphs (E ≈ V or E << V²). For dense graphs, Prim's is often faster.

## Tips for Best Results

1. **Use for sparse graphs:** Kruskal's excels when E is small relative to V²

2. **Pre-sorted edges:** If edges come sorted, skip sorting step for O(E) time!

3. **Understand Union-Find:** Key to appreciating the algorithm's efficiency

4. **Compare with Prim's:** Try both to see which performs better for your graph

## Troubleshooting

### "Graph is disconnected"

**Solution:** Use option to find MST forest (one MST per component).

### Different MST on repeated runs

**Explanation:** If edges have equal weights, tie-breaking may vary. All MSTs have same total cost.

### Slow for large dense graphs

**Recommendation:** Use Prim's algorithm instead for dense graphs (E ≈ V²).

## Advanced Exploration

### Experiment 1: Compare with Prim's

Create the same network and compare:
1. Kruskal's: Global edge sorting
2. Prim's: Local vertex growth

**Observation:** Same MST cost, different construction order!

### Experiment 2: Equal Weight Edges

```
Connection: A B 10
Connection: B C 10
Connection: A C 10
```

**Result:** Multiple valid MSTs (all cost 20). Algorithm picks one.

### Experiment 3: Disconnected Graph

```
Component 1: A-B-C
Component 2: D-E-F
(No edges between components)
```

**Result:** Two separate MSTs (Minimum Spanning Forest).

## Further Reading

- **Original Paper:** Kruskal, J.B. (1956). "On the shortest spanning subtree of a graph"
- **Union-Find:** Tarjan, R.E. (1975). "Efficiency of a good but not linear set union algorithm"
- **Core Implementation:** `../core/kruskals_mst.py`
- **Theory:** `../docs/logic.md`
- **Complexity:** `../docs/complexity.md`

## License

Part of the Algorithm Library collection. See repository LICENSE.

---

**Happy Edge Sorting! 📊🌳**
