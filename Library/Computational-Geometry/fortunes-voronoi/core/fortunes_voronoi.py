import heapq
from typing import List, Tuple, Optional, Set

class Point:
    """Represents a 2D coordinate for geometry calculations."""
    def __init__(self, x: float, y: float) -> None:
        self.x = float(x)
        self.y = float(y)

    def __repr__(self) -> str:
        return f"({self.x:.4f}, {self.y:.4f})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return False
        return abs(self.x - other.x) < 1e-9 and abs(self.y - other.y) < 1e-9

    def __hash__(self) -> int:
        return hash((round(self.x, 9), round(self.y, 9)))


class VoronoiEdge:
    """Represents a Voronoi edge separating two sites."""
    def __init__(self, site_left: Point, site_right: Point) -> None:
        self.site_left = site_left
        self.site_right = site_right
        self.start: Optional[Point] = None
        self.end: Optional[Point] = None

    def __repr__(self) -> str:
        return f"Edge(Sites: {self.site_left} | {self.site_right}, Start: {self.start}, End: {self.end})"


class Arc:
    """Represents a parabolic arc in the beach line (doubly-linked list node)."""
    def __init__(self, site: Point) -> None:
        self.site = site
        self.prev: Optional['Arc'] = None
        self.next: Optional['Arc'] = None
        self.left_edge: Optional[VoronoiEdge] = None
        self.right_edge: Optional[VoronoiEdge] = None
        self.circle_event: Optional['Event'] = None


class Event:
    """Represents an event in the sweep-line queue."""
    def __init__(self, x: float, y: float, type_str: str, site: Optional[Point] = None, arc: Optional[Arc] = None, center: Optional[Point] = None) -> None:
        self.x = x
        self.y = y
        self.type = type_str  # 'site' or 'circle'
        self.site = site      # For site events
        self.arc = arc        # For circle events (arc that disappears)
        self.center = center  # For circle events (center of the circle)
        self.valid = True

    def __lt__(self, other: 'Event') -> bool:
        # Process from top to bottom (decreasing y)
        if abs(self.y - other.y) > 1e-9:
            return self.y > other.y
        # Tie-breaker: left to right (increasing x)
        return self.x < other.x


def get_breakpoint(p1: Point, p2: Point, L: float) -> float:
    """
    Computes the x-coordinate of the breakpoint between two adjacent arcs 
    for sites p1 (left) and p2 (right) when the sweep line is at L.
    """
    x1, y1 = p1.x, p1.y
    x2, y2 = p2.x, p2.y

    # Degenerate cases when a site is on the sweep line
    if abs(y1 - L) < 1e-9:
        return x1
    if abs(y2 - L) < 1e-9:
        return x2

    if abs(y1 - y2) < 1e-9:
        return (x1 + x2) / 2.0

    # Solve quadratic equation Ax^2 + Bx + C = 0
    a1 = 1.0 / (y1 - L)
    a2 = 1.0 / (y2 - L)

    A = a1 - a2
    B = -2.0 * (x1 * a1 - x2 * a2)
    C = a1 * (x1 * x1) - a2 * (x2 * x2) + y1 - y2

    discriminant = B * B - 4.0 * A * C
    if discriminant < 0:
        return (x1 + x2) / 2.0

    sqrt_d = discriminant ** 0.5
    r1 = (-B - sqrt_d) / (2.0 * A)
    r2 = (-B + sqrt_d) / (2.0 * A)

    # Left-to-right arc transition:
    # If p1 is higher (y1 > y2), transition is at the smaller root.
    # If p1 is lower (y1 < y2), transition is at the larger root.
    if y1 > y2:
        return min(r1, r2)
    else:
        return max(r1, r2)


def get_circumcircle(pa: Point, pb: Point, pc: Point) -> Optional[Tuple[Point, float]]:
    """Computes the circumcenter and radius of three 2D points."""
    d = 2 * (pa.x * (pb.y - pc.y) + pb.x * (pc.y - pa.y) + pc.x * (pa.y - pb.y))
    if abs(d) < 1e-9:
        return None

    ux = ((pa.x**2 + pa.y**2) * (pb.y - pc.y) + 
          (pb.x**2 + pb.y**2) * (pc.y - pa.y) + 
          (pc.x**2 + pc.y**2) * (pa.y - pb.y)) / d
          
    uy = ((pa.x**2 + pa.y**2) * (pc.x - pb.x) + 
          (pb.x**2 + pb.y**2) * (pa.x - pc.x) + 
          (pc.x**2 + pc.y**2) * (pb.x - pa.x)) / d

    center = Point(ux, uy)
    r = ((pa.x - ux)**2 + (pa.y - uy)**2)**0.5
    return center, r


def is_clockwise(pa: Point, pb: Point, pc: Point) -> bool:
    """Returns True if the three points form a clockwise turn."""
    val = (pb.x - pa.x) * (pc.y - pb.y) - (pb.y - pa.y) * (pc.x - pb.x)
    return val < -1e-9


def clip_segment(p1: Point, p2: Point, bbox: Tuple[float, float, float, float]) -> Optional[Tuple[Point, Point]]:
    """Clips a line segment to a bounding box [xmin, xmax, ymin, ymax] using Liang-Barsky."""
    xmin, xmax, ymin, ymax = bbox
    x1, y1 = p1.x, p1.y
    x2, y2 = p2.x, p2.y

    dx = x2 - x1
    dy = y2 - y1

    t0, t1 = 0.0, 1.0
    p = [-dx, dx, -dy, dy]
    q = [x1 - xmin, xmax - x1, y1 - ymin, ymax - y1]

    for i in range(4):
        if abs(p[i]) < 1e-9:
            if q[i] < 0:
                return None
        else:
            t = q[i] / p[i]
            if p[i] < 0:
                if t > t1:
                    return None
                elif t > t0:
                    t0 = t
            else:
                if t < t0:
                    return None
                elif t < t1:
                    t1 = t

    if t0 > t1:
        return None

    return (
        Point(x1 + t0 * dx, y1 + t0 * dy),
        Point(x1 + t1 * dx, y1 + t1 * dy)
    )


class VoronoiDiagram:
    """Stores the final Voronoi Diagram result containing sites, vertices, and edges."""
    def __init__(self, sites: List[Point]) -> None:
        self.sites = sites
        self.vertices: List[Point] = []
        self.edges: List[VoronoiEdge] = []


def fortunes_algorithm(sites_input: List[Point], bbox_margin: float = 10.0) -> VoronoiDiagram:
    """
    Executes Fortune's Algorithm to generate a Voronoi Diagram.
    
    Time Complexity: O(N log N)
    Space Complexity: O(N)
    """
    # 1. Preprocess and deduplicate sites
    seen: Set[Tuple[float, float]] = set()
    sites: List[Point] = []
    for s in sites_input:
        coord = (s.x, s.y)
        if coord not in seen:
            seen.add(coord)
            sites.append(s)

    diagram = VoronoiDiagram(sites)
    if len(sites) < 2:
        return diagram

    # Determine bounding box
    xs = [s.x for s in sites]
    ys = [s.y for s in sites]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    
    # If all points are collinear, handle bounding box padding
    dx = xmax - xmin if xmax != xmin else 1.0
    dy = ymax - ymin if ymax != ymin else 1.0
    
    # Add a bounding box margin
    margin_x = max(dx * 0.5, bbox_margin)
    margin_y = max(dy * 0.5, bbox_margin)
    bbox = (
        xmin - margin_x,
        xmax + margin_x,
        ymin - margin_y,
        ymax + margin_y
    )

    # Event Queue
    queue: List[Event] = []
    for s in sites:
        heapq.heappush(queue, Event(s.x, s.y, 'site', site=s))

    # Beach Line doubly-linked list
    beach_line: Optional[Arc] = None

    def check_circle_event(arc: Arc, L: float) -> None:
        """Checks if three adjacent arcs form a circle event."""
        if not arc.prev or not arc.next:
            return
        
        pa, pb, pc = arc.prev.site, arc.site, arc.next.site
        
        # Must turn clockwise to converge
        if not is_clockwise(pa, pb, pc):
            return

        circle_info = get_circumcircle(pa, pb, pc)
        if not circle_info:
            return

        center, radius = circle_info
        event_y = center.y - radius

        # Only check future circle events
        if event_y < L + 1e-9:
            # If there's an existing circle event, invalidate it
            if arc.circle_event:
                arc.circle_event.valid = False
            
            event = Event(center.x, event_y, 'circle', arc=arc, center=center)
            arc.circle_event = event
            heapq.heappush(queue, event)

    # 2. Main Event Loop
    while queue:
        event = heapq.heappop(queue)
        if not event.valid:
            continue

        L = event.y

        if event.type == 'site':
            new_site = event.site
            assert new_site is not None
            
            # If beach line is empty, initialize it
            if beach_line is None:
                beach_line = Arc(new_site)
                continue

            # Find arc directly above new site's x coordinate
            curr = beach_line
            target_arc = None
            while curr:
                # Find boundaries
                x_left = -float('inf')
                x_right = float('inf')
                
                if curr.prev:
                    x_left = get_breakpoint(curr.prev.site, curr.site, L)
                if curr.next:
                    x_right = get_breakpoint(curr.site, curr.next.site, L)
                
                if x_left - 1e-9 <= new_site.x <= x_right + 1e-9:
                    target_arc = curr
                    break
                curr = curr.next

            if not target_arc:
                # Fallback to last node if precision issue occurs
                curr = beach_line
                while curr.next:
                    curr = curr.next
                target_arc = curr

            # Invalidate target arc's existing circle event
            if target_arc.circle_event:
                target_arc.circle_event.valid = False

            # Create new arcs: target_arc -> new_arc -> target_arc_copy
            new_arc = Arc(new_site)
            target_arc_copy = Arc(target_arc.site)

            # Insert into doubly-linked list
            target_arc_copy.next = target_arc.next
            if target_arc.next:
                target_arc.next.prev = target_arc_copy
            
            target_arc.next = new_arc
            new_arc.prev = target_arc
            new_arc.next = target_arc_copy
            target_arc_copy.prev = new_arc

            # Create Voronoi edges starting at the split point
            p_target = target_arc.site
            if abs(p_target.y - L) > 1e-9:
                start_y = ((new_site.x - p_target.x) ** 2) / (2.0 * (p_target.y - L)) + (p_target.y + L) / 2.0
            else:
                start_y = new_site.y  # Degenerate case fallback
            
            start_vertex = Point(new_site.x, start_y)
            
            # Create two half-edges separating target_arc and new_arc
            edge1 = VoronoiEdge(target_arc.site, new_site)
            edge2 = VoronoiEdge(new_site, target_arc.site)
            
            edge1.start = start_vertex
            edge2.start = start_vertex
            
            diagram.edges.append(edge1)
            diagram.edges.append(edge2)

            # Assign edges to arcs
            target_arc_copy.right_edge = target_arc.right_edge
            target_arc.right_edge = edge1
            new_arc.left_edge = edge1
            new_arc.right_edge = edge2
            target_arc_copy.left_edge = edge2

            # Check circle events for triplets
            check_circle_event(target_arc, L)
            check_circle_event(target_arc_copy, L)

        else:
            # Circle Event: arc is disappearing
            disappearing_arc = event.arc
            assert disappearing_arc is not None
            assert event.center is not None

            # Create Voronoi vertex
            vertex = event.center
            diagram.vertices.append(vertex)

            # Close the two meeting edges
            if disappearing_arc.left_edge:
                disappearing_arc.left_edge.end = vertex
            if disappearing_arc.right_edge:
                disappearing_arc.right_edge.end = vertex

            # Remove arc from beach line
            prev_arc = disappearing_arc.prev
            next_arc = disappearing_arc.next
            assert prev_arc is not None
            assert next_arc is not None

            # Invalidate circle events for neighbors
            if prev_arc.circle_event:
                prev_arc.circle_event.valid = False
            if next_arc.circle_event:
                next_arc.circle_event.valid = False

            prev_arc.next = next_arc
            next_arc.prev = prev_arc

            # Start a new edge separating prev_arc.site and next_arc.site
            new_edge = VoronoiEdge(prev_arc.site, next_arc.site)
            new_edge.start = vertex
            diagram.edges.append(new_edge)

            prev_arc.right_edge = new_edge
            next_arc.left_edge = new_edge

            # Check circle events for new triplets
            check_circle_event(prev_arc, L)
            check_circle_event(next_arc, L)

    # 3. Post-processing: Clip all edges to the bounding box
    clipped_edges: List[VoronoiEdge] = []
    
    for edge in diagram.edges:
        p1, p2 = edge.start, edge.end
        
        # If the edge has both start and end, clip it
        if p1 is not None and p2 is not None:
            clipped = clip_segment(p1, p2, bbox)
            if clipped:
                new_edge = VoronoiEdge(edge.site_left, edge.site_right)
                new_edge.start = clipped[0]
                new_edge.end = clipped[1]
                clipped_edges.append(new_edge)
                
        # If the edge has a start but no end (infinite ray extending downwards)
        elif p1 is not None and p2 is None:
            L_far = bbox[2] - 100.0
            x_far = get_breakpoint(edge.site_left, edge.site_right, L_far)
            
            p = edge.site_left
            if abs(p.y - L_far) > 1e-9:
                y_far = ((x_far - p.x) ** 2) / (2.0 * (p.y - L_far)) + (p.y + L_far) / 2.0
            else:
                y_far = L_far
                
            p_far = Point(x_far, y_far)
            clipped = clip_segment(p1, p_far, bbox)
            if clipped:
                new_edge = VoronoiEdge(edge.site_left, edge.site_right)
                new_edge.start = clipped[0]
                new_edge.end = clipped[1]
                clipped_edges.append(new_edge)
                
        # If the edge has neither start nor end (infinite line separating two sites)
        elif p1 is None and p2 is None:
            L_far = bbox[2] - 100.0
            x_far = get_breakpoint(edge.site_left, edge.site_right, L_far)
            p = edge.site_left
            y_far = ((x_far - p.x) ** 2) / (2.0 * (p.y - L_far)) + (p.y + L_far) / 2.0
            p_far = Point(x_far, y_far)
            
            L_near = bbox[3] + 100.0
            x_near = get_breakpoint(edge.site_left, edge.site_right, L_near)
            y_near = ((x_near - p.x) ** 2) / (2.0 * (p.y - L_near)) + (p.y + L_near) / 2.0
            p_near = Point(x_near, y_near)
            
            clipped = clip_segment(p_far, p_near, bbox)
            if clipped:
                new_edge = VoronoiEdge(edge.site_left, edge.site_right)
                new_edge.start = clipped[0]
                new_edge.end = clipped[1]
                clipped_edges.append(new_edge)

    diagram.edges = clipped_edges
    return diagram
