# Algorithm Engineering Library: Theory to Production

A comprehensive, engineer-focused repository dedicated to mastering **World-Famous and Trending Algorithms**. This project bridges the gap between abstract mathematical logic and high-performance, real-world system applications.

## Project Philosophy

Most algorithm repositories are just collections of code snippets. This project treats every algorithm as a **Modular Package**, including:

1. **The Logic:** Optimized implementation in [Language].
2. **The Math:** Formal complexity analysis using Big O notation.
3. **The Application:** A mini-project demonstrating how the algorithm solves a real-world scenario (e.g., Load balancing, GPS routing, or ML-based recommendations).

---

## Repository Architecture

The repository follows a strict modular hierarchy to ensure scalability and ease of exploration.

```text
.
├── categories/
│   ├── graph-theory/              # Algorithms for network & relationship data
│   ├── dynamic-programming/       # Optimization and recursive solutions
│   ├── machine-learning/          # Trending ML logic (Transformers, KNN, etc.)
│   ├── distributed-systems/       # Consensus and consistency (Raft, Paxos)
│   └── data-compression/          # Efficient storage (Huffman, LZ77)
│
├── templates/
│   ├── algorithm_logic.ext        # Standardized code boilerplate
│   └── doc_template.md            # Standardized documentation format
│
├── .github/                       # CI/CD Workflows for automated testing
├── README.md                      # Project Entry Point (Current File)
└── CONTRIBUTING.md                # Guidelines for new implementations

```

### Inside each Algorithm Folder:

Every sub-directory (e.g., `/categories/graph-theory/dijkstra/`) is a standalone learning unit:

* `core/`: The optimized source code.
* `docs/`: Deep-dive analysis ( complexity, edge cases).
* `test-project/`: A practical mini-application using the algorithm.

---

## MIT License

Copyright (c) 2026 Chanuka Ekanayake

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.