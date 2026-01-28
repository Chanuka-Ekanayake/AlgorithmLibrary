# User Guide: Cloud Resource Optimizer (0/1 Knapsack)

This simulator applies Dynamic Programming to solve a common infrastructure problem: **Maximizing ROI on limited hardware.**

## How it Works
The application treats your **GPU VRAM** as a "Knapsack." Each ML model in the `data.json` catalog has a "Weight" (VRAM usage) and a "Value" (Revenue). The algorithm calculates the most profitable combination of models that fits on the server.

## Instructions
1. Navigate to the `test-project` directory.
2. Run the application:
   ```bash
   python app.py