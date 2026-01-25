import sys
import os
import time
from warehouse_grid import WAREHOUSE_STANDARD

# Add the parent directory to the path to import the core logic
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.astar import astar_search

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def render_grid(grid, path=None, start=None, end=None):
    """
    Renders the grid to the console using professional ASCII notation.
    S = Start | G = Goal | * = Path | # = Obstacle
    """
    print("  " + " ".join([str(i) for i in range(len(grid[0]))])) # Col numbers
    for r in range(len(grid)):
        row_output = f"{r} "
        for c in range(len(grid[0])):
            if (r, c) == start:
                row_output += "S "
            elif (r, c) == end:
                row_output += "G "
            elif path and (r, c) in path:
                row_output += "* "
            elif grid[r][c] == 1:
                row_output += "# "
            else:
                row_output += ". "
        print(row_output)

def run_simulation():
    clear_screen()
    print("--------------------------------------------------")
    print("SYSTEM: A-STAR PATHFINDING NAVIGATOR")
    print("STATUS: INITIALIZING GRID CONFIGURATION")
    print("--------------------------------------------------\n")

    start_coord = (0, 0)
    end_coord = (9, 9)

    print("Current Warehouse Map Layout:")
    render_grid(WAREHOUSE_STANDARD, start=start_coord, end=end_coord)
    
    input("\nExecute pathfinding calculation (Press Enter)...")

    # Algorithm Execution
    start_time = time.time()
    result_path = astar_search(WAREHOUSE_STANDARD, start_coord, end_coord)
    latency = (time.time() - start_time) * 1000

    clear_screen()
    if result_path:
        print(f"SUCCESS: Path identified in {latency:.4f}ms.")
        print(f"METRICS: Path consists of {len(result_path)} coordinates.\n")
        render_grid(WAREHOUSE_STANDARD, path=result_path, start=start_coord, end=end_coord)
        print("\nLEGEND: [S] Start | [G] Goal | [*] Optimized Path | [#] Obstacle")
    else:
        print("FAILURE: No viable path exists within grid boundaries.")

    print("\n--------------------------------------------------")
    print("END OF SIMULATION")
    print("--------------------------------------------------")

if __name__ == "__main__":
    run_simulation()