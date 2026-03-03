# User Guide: Route Optimisation Engine (Simulated Annealing)

This project demonstrates **Simulated Annealing** solving the **Travelling Salesman Problem (TSP)**. Ten cities are placed on a known geometric circle so the mathematically optimal tour distance is precomputed — letting you see exactly how close the algorithm gets.

## How to Test

1. **Navigate** to the `test-project` folder.
2. **Run** the simulator:
   ```bash
   python app.py
   ```

## What to Experiment With

| Hyperparameter | File Location | Effect |
|---|---|---|
| `COOLING_RATE` | `app.py` | Lower → slower cool → better quality |
| `INITIAL_TEMP` | `app.py` | Must be high enough to accept early bad moves |
| `ITERATIONS_PER_TEMP` | `app.py` | More → more thorough search at each step |
| `NUM_CITIES` | `app.py` | Increase to make the problem harder |
