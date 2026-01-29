# User Guide: Regional Network Optimizer

This module uses **Kruskal's Algorithm** to solve the Minimum Spanning Tree (MST) problem for infrastructure design.

## How it Works
The algorithm treats cities as **Nodes** and potential fiber routes as **Edges**. By sorting these routes by cost and using a **Disjoint Set Union (DSU)** to avoid loops, it identifies the cheapest possible way to ensure every city can communicate with every other city in the network.

## Instructions
1. Navigate to the `test-project` directory.
2. Run the application:
   ```bash
   python app.py