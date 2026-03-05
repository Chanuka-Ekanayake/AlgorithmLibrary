# Kosaraju's Algorithm (Strongly Connected Components)

## 1. Overview

When your platform distributes complex software packages and interlinked Machine Learning models, dependency management is critical. If Module A requires Module B, and Module B mistakenly requires Module A, you have created a circular dependency. If a buyer attempts to install this bundle, their package manager will freeze in an infinite loop.

**Kosaraju's Algorithm** is an elegant, industrial-grade graph theory engine used to identify Strongly Connected Components (SCCs). By executing a highly coordinated two-pass Depth-First Search (DFS) and mathematically reversing the dependency graph, it perfectly slices a massive catalog into isolated clusters, instantly flagging catastrophic dependency loops before they reach the customer.

---

## 2. Technical Features

- **Two-Pass DFS Architecture:** Avoids the massive CPU overhead of brute-force cycle detection by using a first pass to establish a strict topological "finishing order," and a second pass to extract the clusters.
- **Graph Transposition:** Mathematically reverses every directional dependency in the catalog. During the second DFS pass, this transposition physically traps the search algorithm inside the cyclic loops, perfectly isolating the broken components.
- **Linear Time Execution:** Processes complex, highly dense software catalogs in strict linear time, making it efficient enough to run as an automated continuous integration (CI) check on your backend server.
- **Native String Mapping:** Operates directly on string-based module names natively, bypassing the need for integer-conversion layers and directly integrating with your platform's database architecture.

---

## 3. Architecture

```text
.
├── core/                  # Dependency Resolution Engine
│   ├── __init__.py        # Package initialization
│   └── analyzer.py        # Two-Pass DFS and Transposition logic
├── docs/                  # Technical Documentation
│   ├── logic.md           # The Finishing Stack and reverse-graph trapping mechanics
│   └── complexity.md      # The mathematical advantage over brute-force cycle detection
├── test-project/          # Software Dependency Cluster Analyzer Simulator
│   ├── app.py             # Audits a simulated ML module catalog for circular loops
│   └── instructions.md    # Guide for evaluating catalog health and cluster outputs
└── README.md              # Documentation Entry Point

```

---

## 4. Performance Specifications

Let $V$ represent the number of software modules (Vertices) and $E$ represent the number of dependencies (Edges).

| Metric               | Specification | Description                                                                     |
| -------------------- | ------------- | ------------------------------------------------------------------------------- |
| **Time Complexity**  | $O(V + E)$    | Executes two complete passes, strictly bounding operations to the catalog size. |
| **Space Complexity** | $O(V + E)$    | Requires memory to store both the forward and mathematically reversed graphs.   |
| **Cluster Accuracy** | 100%          | Mathematically guaranteed to isolate all cycles accurately.                     |

---

## 5. Deployment & Usage

### Integration

The `DependencyAnalyzer` can be imported to run automated health checks on your product catalog prior to generating user download bundles:

```python
from core.analyzer import DependencyAnalyzer

# 1. Initialize the audit engine
audit = DependencyAnalyzer()

# 2. Feed the catalog dependencies into the engine
audit.add_dependency("Web-Dashboard", "Auth-Service")
audit.add_dependency("Auth-Service", "Database-Driver")

# 3. Inject a circular dependency (Auth <-> Database)
audit.add_dependency("Database-Driver", "Auth-Service")

# 4. Extract the clusters
clusters = audit.analyze_catalog()

# 5. Evaluate the catalog health
for cluster in clusters:
    if len(cluster) > 1:
        print(f"FATAL: Circular Dependency Detected -> {cluster}")
# Output: FATAL: Circular Dependency Detected -> ['Auth-Service', 'Database-Driver']

```

### Running the Simulator

To observe the engine parsing a complex mock catalog and instantly trapping a hidden 3-part dependency loop:

1. Navigate to the `test-project` directory:

```bash
cd test-project

```

2. Run the Dependency Analyzer Simulator:

```bash
python app.py

```

---

## 6. Industrial Applications

- **Package Managers (NPM, pip, Maven):** Auditing software registry uploads to prevent developers from publishing broken, self-referential packages.
- **Microservice Orchestration:** Mapping the exact dependency order for booting up dozens of interconnected cloud services without deadlocking.
- **Build Systems (Make, Bazel):** Determining which source code files can be compiled in parallel and which must wait for prior dependencies to finish compiling.
