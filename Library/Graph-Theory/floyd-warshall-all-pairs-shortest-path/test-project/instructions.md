# Test Project: City Logistics Network Analyzer

## Overview

This interactive application demonstrates the **Floyd-Warshall algorithm** by analyzing multi-city transportation networks. It simulates a logistics planning system that helps optimize routes, identify strategic hub locations, and analyze network connectivity.

---

## What is All-Pairs Shortest Path?

Unlike single-source algorithms (Dijkstra, Bellman-Ford) that find paths from one starting point, Floyd-Warshall computes the shortest path between **every pair** of cities in one execution. This is essential for:

- **Logistics planning:** Understanding all possible routes
- **Hub optimization:** Finding the best central location
- **Network analysis:** Measuring connectivity and efficiency

---

## How to Run

### Prerequisites

- Python 3.7 or higher
- No external dependencies required

### Running the Application

```bash
# Navigate to the test-project directory
cd test-project

# Run the application
python app.py
```

---

## Features

### 1. Network Analysis from File

Load a predefined city network from `city_network.txt` and perform comprehensive analysis.

**Menu Option:** 1

**Capabilities:**
1. **Distance Matrix:** Complete table showing shortest distance between every city pair
2. **Route Finder:** Find optimal path between any two cities
3. **Hub Optimizer:** Identify the best location for a central warehouse
4. **Network Diameter:** Measure the "worst-case" distance in the network
5. **Connectivity Analysis:** Check which cities can reach which others
6. **All Routes from Source:** View all paths from a specific city

### 2. Manual Network Builder

Create custom networks for testing and education.

**Menu Option:** 2

**Use Cases:**
- Test theoretical scenarios
- Educational demonstrations
- Validate algorithm behavior

---

## Understanding the Data File

### File Format: `city_network.txt`

```
FROM TO COST
```

**Example:**
```
NYC BOS 215    # New York to Boston: 215 km
BOS PHI 300    # Boston to Philadelphia: 300 km
PHI NYC 100    # Philadelphia to New York: 100 km
```

### What "COST" Represents

The cost value can represent:
- **Distance** (kilometers/miles)
- **Time** (minutes/hours)
- **Money** (dollars/euros)
- **Any metric** you want to minimize

---

## Example Usage Sessions

### Session 1: Finding Optimal Route

```
Select option: 2 (Find shortest route)

From city: NYC
To city: LA

✓ Shortest route from NYC to LA:
  Distance: 2790
  Path: NYC → CHI → LA
```

**Interpretation:** Instead of the direct NYC→LA route (2800), it's shorter to go via Chicago (2790).

### Session 2: Finding Best Hub

```
Select option: 3 (Find optimal hub location)

🎯 FINDING OPTIMAL HUB LOCATION...

✓ Optimal hub: CHI
  Maximum distance to any city: 2020

  Interpretation: Placing your main warehouse in CHI
  ensures no destination is farther than 2020 units away.
```

**Use Case:** Minimizes worst-case delivery distance.

### Session 3: Network Diameter

```
Select option: 4 (Calculate network diameter)

✓ Network diameter: 3615

  Interpretation: The worst-case distance between any two
  connected cities is 3615 units.
```

**Metric:** Measures network "span" - useful for planning maximum delivery times.

---

## How Floyd-Warshall Works in This Context

### Algorithm Steps

1. **Initialization:**
   - Load all city connections
   - Create distance matrix (initially ∞ for unconnected cities)
   - Set direct connections to their given costs

2. **Main Iteration:**
   - For each city k (as potential intermediate):
     - For every pair of cities (i, j):
       - Check if route i→k→j is shorter than direct i→j
       - Update if improvement found

3. **Result:**
   - Complete matrix showing shortest distance for all pairs
   - Next-hop information for path reconstruction

### Example Evolution

**Initial (direct connections only):**
```
     NYC  BOS  PHI
NYC   0   215  95
BOS  220   0   300
PHI  100  295   0
```

**After considering PHI as intermediate:**
```
     NYC  BOS  PHI
NYC   0   195  95   ← NYC→PHI→BOS (95+100=195) better than direct (215)
BOS  220   0   300
PHI  100  295   0
```

---

## Understanding the Outputs

### 1. Distance Matrix

Shows the minimum cost from any city (row) to any city (column):

```
       NYC  BOS  LA  CHI
  NYC   0   215  2790 790
  BOS  220   0   3010 1010
  LA  2790 3010  0   2010
  CHI  785  1005 2015  0
```

**Reading:** To go from BOS to LA, shortest distance is 3010 via intermediate cities.

### 2. Path Reconstruction

```
NYC → LA: 2790 via NYC → CHI → LA
```

Shows not just the distance, but the actual route to take.

### 3. Graph Center

The city that minimizes the maximum distance to all others:

**Algorithm:**
- For each city, find its **eccentricity** (max distance to any other city)
- City with minimum eccentricity is the center

**Use:** Optimal location for distribution hubs, emergency services, etc.

### 4. Network Diameter

Maximum shortest path length in the network:

```
diameter = max(distance[i][j] for all i, j)
```

**Use:** Measures network efficiency - smaller diameter = better connectivity.

### 5. Transitive Closure

Boolean matrix showing reachability:

```
     NYC  BOS  LA
NYC   ✓    ✓   ✓
BOS   ✓    ✓   ✓
LA    ✓    ✓   ✓
```

**✓** = Can reach, **✗** = Cannot reach

---

## Real-World Applications

### 1. Logistics & Supply Chain

**Scenario:** Distribution company with 20 regional warehouses

**Questions Floyd-Warshall Answers:**
- What's the fastest route from any warehouse to any other?
- Where should we build our central hub?
- Which warehouse pairs have the worst connectivity?

### 2. Network Routing

**Scenario:** Internet backbone with routers in major cities

**Usage:**
- Precompute routing tables for all router pairs
- Identify network bottlenecks (high eccentricity nodes)
- Plan redundancy for critical paths

### 3. Urban Planning

**Scenario:** City planning for public transportation

**Analysis:**
- Which neighborhoods have poor connectivity?
- Where to locate emergency services for optimal coverage?
- Measure network diameter to ensure max travel time bounds

### 4. Social Network Analysis

**Scenario:** Six degrees of separation analysis

**Metrics:**
- Closeness centrality (inverse of average distance to others)
- Network diameter (maximum degrees of separation)
- Identify influential nodes (low eccentricity)

---

## Testing Different Scenarios

### Create a Hub-and-Spoke Network

```
# All cities connect through Chicago hub
NYC CHI 790
BOS CHI 1005
LA CHI 2015
SF CHI 2150
...
CHI NYC 785
CHI BOS 1010
CHI LA 2010
...
```

**Observation:** CHI will be the perfect center with eccentricity = max spoke length.

### Test Disconnected Network

```
# East coast cities
NYC BOS 215
BOS PHI 300

# West coast cities (no connection to east)
LA SF 380
SF SEA 810
```

**Result:** Infinite distances between coasts, low connectivity percentage.

### Create Triangular Arbitrage (Negative Cycle)

```
NYC BOS 100
BOS PHI 50
PHI NYC -200  # Impossible: traveling in circle reduces cost!
```

**Result:** Algorithm detects negative cycle, warns user.

---

## Performance Characteristics

### Time Complexity

**O(V³)** where V = number of cities

| Cities | Iterations | Time |
|--------|-----------|------|
| 10 | 1,000 | <1 ms |
| 50 | 125,000 | 10 ms |
| 100 | 1,000,000 | 100 ms |
| 500 | 125,000,000 | 10 sec |

### Memory Usage

**O(V²)** for distance and next-hop matrices

| Cities | Pairs | Memory |
|--------|-------|--------|
| 10 | 100 | <1 KB |
| 100 | 10,000 | ~80 KB |
| 500 | 250,000 | ~2 MB |

---

## Extending the Application

### Ideas for Enhancement

1. **Visualization:**
   - Plot city network as a graph
   - Highlight optimal paths
   - Animate algorithm execution

2. **Real Data Integration:**
   - Load actual city coordinates
   - Calculate distances from GPS data
   - Fetch real-time traffic/flight data

3. **Multi-Criteria Optimization:**
   - Consider both distance and cost
   - Time windows for deliveries
   - Capacity constraints

4. **Comparison Mode:**
   - Compare Floyd-Warshall with Dijkstra
   - Benchmark performance on different graph types

---

## Common Questions

### Q: Why use Floyd-Warshall instead of running Dijkstra multiple times?

**A:** For dense networks, Floyd-Warshall can be more efficient:
- Dense network: Floyd-Warshall O(V³) vs Dijkstra×V O(V³ log V)
- Simpler implementation
- Better for negative weights (if applicable)

For sparse networks, Dijkstra is better.

### Q: Can I use negative costs?

**A:** Yes! Floyd-Warshall handles negative edge weights correctly and detects negative cycles (impossible scenarios).

### Q: What if two cities aren't connected?

**A:** Distance remains ∞, and "No route available" is displayed.

---

## Troubleshooting

### "File not found" Error

The app automatically creates `city_network.txt` with sample data if missing.

### "Invalid format" Warning

Ensure each line in the file follows: `FROM TO COST`
- Space-separated (no commas)
- Uppercase city codes (automatically converted)
- Numeric cost value

### Slow Performance

With 500+ cities, computation may take 10+ seconds. This is normal for O(V³) complexity.

---

## Educational Value

### What This Demonstrates

1. **Dynamic Programming:** Building solutions from subproblems
2. **All-Pairs Shortest Path:** Complete network distance analysis
3. **Graph Metrics:** Diameter, center, connectivity
4. **Path Reconstruction:** Tracing optimal routes
5. **Real-World Modeling:** Logistics and network planning

### Key Concepts

- **Optimal Substructure:** Shortest paths contain shortest subpaths
- **Systematic Exploration:** Consider each vertex as intermediate
- **Matrix Representation:** Efficient storage of all-pairs data
- **Network Centrality:** Identifying strategic nodes

---

## Summary

This test project brings Floyd-Warshall to life by solving practical logistics problems:

✅ **Comprehensive analysis** of all city pairs  
✅ **Hub optimization** for strategic planning  
✅ **Network metrics** for performance evaluation  
✅ **Interactive exploration** of algorithm behavior

Experiment with different networks and discover how Floyd-Warshall provides complete visibility into network connectivity and optimal routing!
