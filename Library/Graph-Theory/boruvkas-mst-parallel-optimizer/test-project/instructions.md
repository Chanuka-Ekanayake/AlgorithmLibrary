# User Guide: Global Data Center Network Optimizer

This module uses **Borůvka's Algorithm** to solve the Minimum Spanning Tree (MST) problem for global infrastructure design.

## How it Works

The algorithm treats data center locations as **Nodes** and potential submarine/land cable routes as **Edges**. In each round, every connected component independently identifies its cheapest outgoing link to another component. All cheapest links are merged simultaneously, halving the number of components each round.

This **component-merging** strategy is what makes Borůvka's uniquely suited for parallel and distributed execution — each component's search is independent.

## Prerequisites

- Python 3.8 or higher
- No external dependencies required (uses standard library only)

## Instructions

1. Navigate to the `test-project` directory:
   ```bash
   cd test-project
   ```

2. Run the application:
   ```bash
   python app.py
   ```

## Expected Output

The application will:

1. **Load** 8 global data center hub locations and 15 potential cable routes from `network_data.json`.
2. **Verify** that the network is connected (MST exists).
3. **Execute** Borůvka's MST algorithm to find the optimal cable layout.
4. **Report** the selected routes, total cost, savings analysis, and network statistics.

## Scenarios Demonstrated

### Global Submarine Cable Network
- **Nodes:** San Francisco, New York, London, Frankfurt, Tokyo, Singapore, Sydney, São Paulo
- **Edges:** Potential high-speed fiber-optic cable routes with costs in millions of dollars
- **Goal:** Connect all 8 hubs with minimum total cable cost

### Key Metrics Reported
- **Total Infrastructure Investment:** Minimum cost to connect all hubs
- **Cost Savings:** Comparison vs. building all possible routes
- **Network Diameter:** Maximum latency path through the MST
- **Cable Statistics:** Min, max, and average cable costs

## Customization

To test with your own network data, modify `network_data.json`:

```json
{
    "nodes": ["HubA", "HubB", "HubC"],
    "potential_connections": [
        {"u": "HubA", "v": "HubB", "cost": 100},
        {"u": "HubB", "v": "HubC", "cost": 200},
        {"u": "HubA", "v": "HubC", "cost": 150}
    ]
}
```
