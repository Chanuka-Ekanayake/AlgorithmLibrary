import heapq
from typing import List, Tuple, Dict, Optional

class Node:
    """Represents a coordinate in the warehouse grid."""
    def __init__(self, x: int, y: int, parent=None):
        self.x = x
        self.y = y
        self.parent = parent
        self.g = 0  # Cost from start to current node
        self.h = 0  # Heuristic (estimated cost to goal)
        self.f = 0  # Total cost (g + h)

    def __lt__(self, other):
        return self.f < other.f

def manhattan_distance(curr: Tuple[int, int], goal: Tuple[int, int]) -> int:
    """The 'Smart Guess': Distance ignoring obstacles."""
    return abs(curr[0] - goal[0]) + abs(curr[1] - goal[1])

def astar_search(grid: List[List[int]], start: Tuple[int, int], end: Tuple[int, int]):
    """
    A* Pathfinding implementation for a 2D Grid.
    0 = Walkable, 1 = Obstacle/Wall
    """
    start_node = Node(start[0], start[1])
    end_node = Node(end[0], end[1])

    open_list = []
    closed_set = set()

    heapq.heappush(open_list, start_node)

    while open_list:
        # Get the node with the lowest f(n)
        current_node = heapq.heappop(open_list)
        closed_set.add((current_node.x, current_node.y))

        # Goal Reached!
        if (current_node.x, current_node.y) == (end_node.x, end_node.y):
            path = []
            while current_node:
                path.append((current_node.x, current_node.y))
                current_node = current_node.parent
            return path[::-1] # Return reversed path

        # Generate Neighbors (Up, Down, Left, Right)
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = current_node.x + dx, current_node.y + dy

            # Boundary and Obstacle Checks
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == 0:
                if (nx, ny) in closed_set:
                    continue

                neighbor = Node(nx, ny, current_node)
                neighbor.g = current_node.g + 1
                neighbor.h = manhattan_distance((nx, ny), (end_node.x, end_node.y))
                neighbor.f = neighbor.g + neighbor.h

                # If this path is better than any previously found, add it
                if any(open_node for open_node in open_list if open_node.x == nx and open_node.y == ny and neighbor.g >= open_node.g):
                    continue

                heapq.heappush(open_list, neighbor)

    return None # No path found