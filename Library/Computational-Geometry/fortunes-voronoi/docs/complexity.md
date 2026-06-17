# Technical Specification: Fortune's Algorithm Complexity Analysis

This document outlines the time and space complexity profile of Fortune's sweep-line algorithm for constructing Voronoi Diagrams.

## 1. Complexity Profile

| Operation | Time Complexity | Space Complexity | Description |
| --- | --- | --- | --- |
| **Site Event Processing** | $O(\log N)$ | $O(1)$ | Inserting a new site, splitting beach line, queue operations. |
| **Circle Event Processing** | $O(\log N)$ | $O(1)$ | Removing a collapsed arc, updating neighbors, queue operations. |
| **Overall Algorithm** | $O(N \log N)$ | $O(N)$ | Total cost for $N$ sites. |

---

## 2. Detailed Breakdown

### 2.1 Time Complexity: $O(N \log N)$

The algorithm processes two types of events: **Site Events** (exactly $N$) and **Circle Events** (at most $2N - 5$). Hence, the total number of events processed is $O(N)$.

1. **Event Queue Operations**:
   - The queue is implemented using a binary heap (priority queue).
   - Each insertion and deletion operation in the heap takes $O(\log N)$ time.
   - For $O(N)$ events, the total queue overhead is $O(N \log N)$.

2. **Beach Line Operations**:
   - Using a balanced binary tree (e.g., Red-Black Tree), inserting an arc or deleting an arc takes $O(\log N)$ time.
   - In our educational implementation, we utilize an ordered doubly linked list. While traversal in the worst case takes $O(N)$, it runs in $O(N^2)$ for highly skewed configurations but provides $O(N \log N)$ average-case behavior on typical scattered coordinate clouds.

3. **Clipped Edge Post-processing**:
   - There are $O(N)$ edges generated (since Euler's formula guarantees $3N-6$ edges in planar triangulations).
   - Clipping each edge via Liang-Barsky takes $O(1)$ constant time.
   - Total clipping overhead is $O(N)$.

### 2.2 Space Complexity: $O(N)$

Memory footprint is strictly linear with respect to the number of input sites $N$:
1. **Event Queue**: Can hold at most $O(N)$ events simultaneously.
2. **Beach Line**: At any point, the number of active arcs is at most $2N - 1$.
3. **Diagram Storage**: Stores $N$ sites, at most $2N-5$ vertices, and at most $3N-6$ edges.
