import sys
import os
import json

# Add parent directory to path for core logic access
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.knapsack import KnapsackOptimizer

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_catalog(filepath):
    """Loads the model catalog from JSON."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return []

def run_optimization_simulation():
    clear_screen()
    print("--------------------------------------------------")
    print("SYSTEM: CLOUD RESOURCE OPTIMIZER (KNAPSACK)")
    print("STATUS: LOADED ML MODEL CATALOG")
    print("--------------------------------------------------\n")

    catalog = load_catalog('data.json')
    if not catalog:
        return

    # Extract values and weights for the algorithm
    names = [item['name'] for item in catalog]
    revenues = [item['revenue'] for item in catalog]
    vram_requirements = [item['vram_gb'] for item in catalog]

    # User Input for Capacity
    print("Available GPU Hardware Profiles:")
    print("1. NVIDIA RTX 4090 (24GB)")
    print("2. NVIDIA A100 (40GB)")
    print("3. NVIDIA H100 (80GB)")
    
    try:
        capacity = int(input("\nEnter the VRAM capacity (GB) for this instance: "))
    except ValueError:
        print("Invalid input. Defaulting to 24GB.")
        capacity = 24

    # Execute Optimization
    optimizer = KnapsackOptimizer()
    max_rev, selected_indices = optimizer.solve(revenues, vram_requirements, capacity)

    # Output Results
    print("\n--------------------------------------------------")
    print(f"OPTIMIZATION COMPLETE FOR {capacity}GB VRAM")
    print("--------------------------------------------------")
    
    if selected_indices:
        print(f"Selected Models for Deployment:")
        total_vram = 0
        for idx in selected_indices:
            model = catalog[idx]
            print(f"  - {model['name']} (VRAM: {model['vram_gb']}GB | Rev: ${model['revenue']})")
            total_vram += model['vram_gb']
        
        print(f"\nFINAL METRICS:")
        print(f"  Total Projected Revenue: ${max_rev}")
        print(f"  VRAM Utilization:        {total_vram}/{capacity} GB ({(total_vram/capacity)*100:.1f}%)")
    else:
        print("No models can fit into the provided capacity.")

    print("--------------------------------------------------")

if __name__ == "__main__":
    run_optimization_simulation()