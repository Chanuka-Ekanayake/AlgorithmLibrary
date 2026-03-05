"""
Kosaraju's Algorithm (Strongly Connected Components)
An industrial-grade dependency resolution engine. It utilizes a highly 
coordinated Two-Pass DFS alongside Graph Transposition to mathematically 
isolate cyclic dependencies and clustered software packages.
"""

from collections import defaultdict
from typing import List, Set, Dict

class DependencyAnalyzer:
    """
    Analyzes software catalog dependencies to find standalone modules,
    cohesive bundles, and catastrophic circular dependency loops.
    """

    def __init__(self):
        # We use dictionaries to support string-based module names natively
        self.graph: Dict[str, List[str]] = defaultdict(list)
        self.transposed_graph: Dict[str, List[str]] = defaultdict(list)
        self.modules: Set[str] = set()

    def add_dependency(self, module: str, requires: str) -> None:
        """
        Registers that 'module' depends on 'requires'.
        Automatically builds the transposed (reversed) graph in parallel.
        """
        self.modules.add(module)
        self.modules.add(requires)
        
        # Forward Edge (Used for Pass 1)
        self.graph[module].append(requires)
        
        # Reversed Edge (Used for Pass 2)
        self.transposed_graph[requires].append(module)

    def _dfs_pass_1(self, node: str, visited: Set[str], finish_stack: List[str]) -> None:
        """
        Phase 1: Deep exploration to establish the topological 'finishing order'.
        Nodes that hit dead-ends are pushed to the stack first.
        """
        visited.add(node)
        
        for neighbor in self.graph[node]:
            if neighbor not in visited:
                self._dfs_pass_1(neighbor, visited, finish_stack)
                
        # Once all dependencies of this node are explored, push it to the stack
        finish_stack.append(node)

    def _dfs_pass_2(self, node: str, visited: Set[str], current_scc: List[str]) -> None:
        """
        Phase 2: Explores the transposed graph. Because the edges are reversed, 
        the DFS gets physically 'trapped' inside the strongly connected component.
        """
        visited.add(node)
        current_scc.append(node)
        
        for neighbor in self.transposed_graph[node]:
            if neighbor not in visited:
                self._dfs_pass_2(neighbor, visited, current_scc)

    def analyze_catalog(self) -> List[List[str]]:
        """
        Executes Kosaraju's Two-Pass Algorithm to find all SCCs.
        Returns a list of clusters. A cluster with >1 module is a circular dependency.
        """
        visited: Set[str] = set()
        finish_stack: List[str] = []

        # Phase 1: Establish Finishing Times
        # We must check every module in case the graph is disconnected
        for module in self.modules:
            if module not in visited:
                self._dfs_pass_1(module, visited, finish_stack)

        # Phase 2: Extract the Clusters
        visited.clear()
        clusters: List[List[str]] = []

        # Process nodes in the exact reverse order of their finishing times
        while finish_stack:
            module = finish_stack.pop()
            
            if module not in visited:
                current_scc: List[str] = []
                self._dfs_pass_2(module, visited, current_scc)
                
                # Sort the cluster alphabetically for clean logging
                current_scc.sort()
                clusters.append(current_scc)

        return clusters