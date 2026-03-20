from typing import List

class Point:
    """
    Represents a 2D coordinate for geometry calculations.
    """
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def __lt__(self, other: 'Point') -> bool:
        """Lexicographical comparison: primarily x, secondarily y."""
        return (self.x, self.y) < (other.x, other.y)

def cross_product(o: Point, a: Point, b: Point) -> float:
    """
    Returns the 2D cross product of vectors OA and OB.
    
    Orientation logic:
    - Positive: Counter-clockwise (left turn)
    - Negative: Clockwise (right turn)
    - Zero: Collinear (linear trajectory)
    
    Args:
        o: Origin point (shared vertex)
        a: Endpoint of vector OA
        b: Endpoint of vector OB
    """
    return (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x)

def monotone_chain(points: List[Point]) -> List[Point]:
    """
    Computes the Convex Hull of a set of 2D points using Andrew's Monotone Chain algorithm.
    
    The algorithm constructs the hull by building the lower and upper boundaries 
    separately, ensuring each turn is strictly counter-clockwise.
    
    Performance:
        - Time Complexity: O(N log N) dominated by the initial lexicographical sort.
        - Space Complexity: O(N) current hull storage during construction.

    Args:
        points: A list of Point objects to envelop.
        
    Returns:
        A list of Point objects forming the vertices of the convex hull 
        in counter-clockwise order.
    """
    n = len(points)
    if n <= 2:
        return sorted(points)

    # 1. Sort points lexicographically (O(N log N))
    sorted_points = sorted(points)

    # 2. Construct the Lower Hull
    lower: List[Point] = []
    for p in sorted_points:
        # While points in 'lower' don't form a counter-clockwise turn with 'p'
        while len(lower) >= 2 and cross_product(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    # 3. Construct the Upper Hull
    upper: List[Point] = []
    for p in reversed(sorted_points):
        # While points in 'upper' don't form a counter-clockwise turn with 'p'
        while len(upper) >= 2 and cross_product(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    # 4. Concatenate boundaries, skipping the last point of each as it overlaps
    return lower[:-1] + upper[:-1]

