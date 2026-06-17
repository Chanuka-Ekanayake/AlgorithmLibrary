# Running the Voronoi Diagram Verification Suite

This project contains the verification tests for Fortune's Sweep-Line algorithm and exports a visual SVG file of the generated Voronoi cell boundaries.

## Prerequisites

- **Python 3.8+** (Standard Library only, no external dependencies required).

## How to Run the Tests

Execute the test suite from the current directory:

```bash
python app.py
```

## Visualizing the Output

Upon successful execution, the script will generate an SVG file in the test-project directory:
- `voronoi_output.svg`

Open `voronoi_output.svg` in any modern web browser (Chrome, Firefox, Edge, Safari) to visually inspect the Voronoi cells, vertices, and input sites.
- **Red Circles:** Input sites (points).
- **Green Circles:** Voronoi vertices (circumcenters of adjacent sites).
- **Blue Lines:** Voronoi edges (cell boundaries).
