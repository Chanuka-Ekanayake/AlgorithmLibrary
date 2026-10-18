# User Guide: Cloud Mesh Ingestion & Pipeline Router (Push-Relabel Algorithm)

This project simulates a high-throughput, cross-region mesh data ingestion pipeline for distributed analytics. It demonstrates the **Push-Relabel Maximum Flow Algorithm (Goldberg-Tarjan)** with Highest-Label selection and the Gap Heuristic to calculate sustained network throughput, link saturation, and critical structural bottlenecks.

## How to Test

1. **Navigate** to the `test-project` directory:
   ```bash
   cd test-project
   ```

2. **Execute** the simulator:
   ```bash
   python app.py
   ```

## What to Observe

- **Sustained Flow Value:** The mathematical upper bound on data transfer from the Gateway to the central Data Lake across all available pathways.
- **Link Saturation Table:** Explicit detection of links running at 100% capacity (`[SATURATED]`) versus those with headroom.
- **Min-Cut Bottleneck Extraction:** Identification of the $(S, T)$ partition cut determining where physical bandwidth expansion yields the highest return on investment.
