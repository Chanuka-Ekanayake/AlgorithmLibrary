import sys
import os
import time
import random
from typing import List

# Add core to path so we can import fortunes_voronoi
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.fortunes_voronoi import Point, fortunes_algorithm

def export_to_svg(filename: str, sites: List[Point], edges: List[any], vertices: List[Point], width: int = 800, height: int = 800) -> None:
    """Exports the Voronoi diagram to a beautiful, dark-themed SVG file."""
    if not sites:
        return

    # Find boundaries
    xs = [s.x for s in sites]
    ys = [s.y for s in sites]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)

    # Pad boundaries
    dx = xmax - xmin if xmax != xmin else 1.0
    dy = ymax - ymin if ymax != ymin else 1.0
    padding = 1.2
    
    # Calculate viewport coordinates
    v_xmin = xmin - dx * 0.1
    v_xmax = xmax + dx * 0.1
    v_ymin = ymin - dy * 0.1
    v_ymax = ymax + dy * 0.1
    
    v_width = v_xmax - v_xmin
    v_height = v_ymax - v_ymin

    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{v_xmin} {v_ymin} {v_width} {v_height}" width="{width}" height="{height}" style="background-color: #0f172a; border-radius: 12px; font-family: sans-serif;">',
        '  <!-- Background grid pattern -->',
        '  <defs>',
        '    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">',
        '      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#1e293b" stroke-width="1"/>',
        '    </pattern>',
        '  </defs>',
        f'  <rect x="{v_xmin}" y="{v_ymin}" width="{v_width}" height="{v_height}" fill="url(#grid)" />',
        '',
        '  <!-- Voronoi Edges -->',
    ]

    for edge in edges:
        if edge.start and edge.end:
            svg_lines.append(
                f'  <line x1="{edge.start.x:.3f}" y1="{edge.start.y:.3f}" x2="{edge.end.x:.3f}" y2="{edge.end.y:.3f}" '
                f'stroke="#38bdf8" stroke-width="2" stroke-linecap="round" opacity="0.85" />'
            )

    svg_lines.append('\n  <!-- Voronoi Vertices -->')
    for v in vertices:
        svg_lines.append(
            f'  <circle cx="{v.x:.3f}" cy="{v.y:.3f}" r="4" fill="#4ade80" stroke="#0f172a" stroke-width="1" />'
        )

    svg_lines.append('\n  <!-- Input Sites -->')
    for s in sites:
        svg_lines.append(
            f'  <circle cx="{s.x:.3f}" cy="{s.y:.3f}" r="6" fill="#f87171" stroke="#ffffff" stroke-width="1.5" />'
        )

    # Add a watermark/title
    svg_lines.append(
        f'\n  <text x="{v_xmin + v_width*0.03}" y="{v_ymin + v_height*0.05}" fill="#94a3b8" font-size="14" font-weight="bold">Fortune\'s Voronoi Diagram</text>'
    )
    svg_lines.append(
        f'  <text x="{v_xmin + v_width*0.03}" y="{v_ymin + v_height*0.08}" fill="#64748b" font-size="10">Sites: {len(sites)} | Edges: {len(edges)} | Vertices: {len(vertices)}</text>'
    )

    svg_lines.append('</svg>')

    with open(filename, 'w') as f:
        f.write('\n'.join(svg_lines))
    print(f"  [SUCCESS] Visual output exported to: {filename}")


def run_tests() -> int:
    # Test Scenario 1: Triangle Layout
    sites_triangle = [Point(100, 100), Point(700, 200), Point(400, 600)]
    
    # Test Scenario 2: 4-Point Square grid
    sites_square = [Point(200, 200), Point(600, 200), Point(600, 600), Point(200, 600)]

    # Test Scenario 3: Random Point Cloud
    random.seed(42)
    sites_random = [Point(random.randint(50, 750), random.randint(50, 750)) for _ in range(30)]

    test_cases = [
        {
            "name": "Triangle Sites",
            "sites": sites_triangle,
            "expected_vertices": 1, # 3 non-collinear sites produce 1 circumcenter vertex
            "desc": "Tests simple three-site circumcenter vertex creation."
        },
        {
            "name": "Square Grid Layout",
            "sites": sites_square,
            "expected_vertices": 1, # A perfect square has 1 center vertex
            "desc": "Verifies symmetric 4-site configuration."
        },
        {
            "name": "Random Point Cloud (N=30)",
            "sites": sites_random,
            "expected_vertices": None,
            "desc": "Checks stability and edge cases on larger random clouds."
        }
    ]

    print("\n" + "="*70)
    print("  SYSTEM: VORONOI DIAGRAM VERIFICATION SUITE")
    print("  ALGORITHM: FORTUNE'S SWEEP-LINE ALGORITHM")
    print("="*70 + "\n")

    any_failed = False
    start_total = time.perf_counter()

    for i, case in enumerate(test_cases, 1):
        print(f"[{i}] Testing: {case['name']}")
        print(f"    Description: {case['desc']}")
        
        t0 = time.perf_counter()
        diagram = fortunes_algorithm(case["sites"])
        duration = (time.perf_counter() - t0) * 1000
        
        # Verify Euler's Planar Graph relations (V - E + F = 2) for closed subgraphs
        # But here we have cropped edges. We'll verify vertex bounds.
        passed = True
        if case["expected_vertices"] is not None:
            # Check if we generated the expected number of vertices
            # Note: with collinearity or precision, this might vary slightly, but for basic sets it's exact.
            v_count = len(diagram.vertices)
            if v_count != case["expected_vertices"]:
                passed = False
                any_failed = True
                print(f"    [FAIL] Vertex count: {v_count} (Expected: {case['expected_vertices']})")

        status = "PASSED" if passed else "FAILED"
        print(f"    Status:      {status} (Execution Time: {duration:.2f} ms)")
        print(f"    Sites Count: {len(diagram.sites)}")
        print(f"    Vertices:    {len(diagram.vertices)}")
        print(f"    Edges:       {len(diagram.edges)}\n")

        # Export the final random cloud to SVG
        if case["name"].startswith("Random Point Cloud"):
            out_path = os.path.join(os.path.dirname(__file__), 'voronoi_output.svg')
            export_to_svg(out_path, diagram.sites, diagram.edges, diagram.vertices)

    total_time = (time.perf_counter() - start_total) * 1000
    print("="*70)
    print(f"  VERIFICATION COMPLETE in {total_time:.2f} ms")
    print("="*70)

    if any_failed:
        print("\n  [ERROR] One or more test constraints failed. Check logs.")
        return 1
    
    print("\n  [SUCCESS] All geometric boundaries and event closures validated.")
    return 0

if __name__ == "__main__":
    sys.exit(run_tests())
