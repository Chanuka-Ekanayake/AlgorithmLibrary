# ACO Simulator Instructions

## Requirements
The simulator uses Python's standard library. No external dependencies (like `numpy` or `scipy`) are required.

## Running the Simulator
1. Open your terminal.
2. Navigate to this directory:
   ```bash
   cd Library/Optimization-Algorithms/ant-colony-optimization/test-project
   ```
3. Run the script:
   ```bash
   python app.py
   ```

## Experimentation
You can modify the following hyper-parameters in `app.py` to see how ACO behaves:
- **`n_ants`**: Increasing this provides wider exploration but linearly increases compute time per iteration.
- **`evaporation_rate` ($\rho$)**: Controls long-term memory. A high $\rho$ mimics "short-term memory" making the algorithm forget old paths quickly, avoiding local minima traps but possibly destabilizing known good paths. 
- **`alpha`**: Determines the weight of the pheromone trail. If set to 0, it behaves like a standard greedy nearest-neighbor search.
- **`beta`**: Determines the weight of distance. If set to 0, ants will only follow pheromones (making them highly vulnerable to bad initial trails).
