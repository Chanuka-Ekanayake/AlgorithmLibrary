from __future__ import annotations

from typing import Iterable, List, Sequence, Tuple


class RangeAddRangeSumSegmentTree:
    def __init__(self, values: Sequence[int]):
        self.n = len(values)
        self.tree = [0] * (4 * self.n if self.n else 1)
        self.lazy = [0] * (4 * self.n if self.n else 1)
        if self.n:
            self._build(1, 0, self.n - 1, values)

    def _build(self, node: int, left: int, right: int, values: Sequence[int]) -> None:
        if left == right:
            self.tree[node] = values[left]
            return

        mid = (left + right) // 2
        self._build(node * 2, left, mid, values)
        self._build(node * 2 + 1, mid + 1, right, values)
        self.tree[node] = self.tree[node * 2] + self.tree[node * 2 + 1]

    def _apply(self, node: int, left: int, right: int, delta: int) -> None:
        self.tree[node] += (right - left + 1) * delta
        self.lazy[node] += delta

    def _push(self, node: int, left: int, right: int) -> None:
        if self.lazy[node] == 0 or left == right:
            return

        mid = (left + right) // 2
        delta = self.lazy[node]
        self._apply(node * 2, left, mid, delta)
        self._apply(node * 2 + 1, mid + 1, right, delta)
        self.lazy[node] = 0

    def _range_add(self, node: int, left: int, right: int, query_left: int, query_right: int, delta: int) -> None:
        if query_left > right or query_right < left:
            return

        if query_left <= left and right <= query_right:
            self._apply(node, left, right, delta)
            return

        self._push(node, left, right)
        mid = (left + right) // 2
        self._range_add(node * 2, left, mid, query_left, query_right, delta)
        self._range_add(node * 2 + 1, mid + 1, right, query_left, query_right, delta)
        self.tree[node] = self.tree[node * 2] + self.tree[node * 2 + 1]

    def _range_sum(self, node: int, left: int, right: int, query_left: int, query_right: int) -> int:
        if query_left > right or query_right < left:
            return 0

        if query_left <= left and right <= query_right:
            return self.tree[node]

        self._push(node, left, right)
        mid = (left + right) // 2
        return self._range_sum(node * 2, left, mid, query_left, query_right) + self._range_sum(
            node * 2 + 1,
            mid + 1,
            right,
            query_left,
            query_right,
        )

    def add(self, left: int, right: int, delta: int) -> None:
        if not self.n:
            return
        self._range_add(1, 0, self.n - 1, left, right, delta)

    def query(self, left: int, right: int) -> int:
        if not self.n:
            return 0
        return self._range_sum(1, 0, self.n - 1, left, right)


class HeavyLightDecomposition:
    def __init__(self, node_count: int, edges: Iterable[Tuple[int, int]], values: Sequence[int] | None = None):
        if node_count <= 0:
            raise ValueError("node_count must be positive")

        self.n = node_count
        self.graph = [[] for _ in range(self.n)]
        for left, right in edges:
            self._validate_node(left)
            self._validate_node(right)
            self.graph[left].append(right)
            self.graph[right].append(left)

        if values is None:
            values = [0] * self.n
        if len(values) != self.n:
            raise ValueError("values must contain exactly node_count elements")

        self.values = list(values)
        self.parent = [-1] * self.n
        self.depth = [0] * self.n
        self.subtree_size = [0] * self.n
        self.heavy_child = [-1] * self.n
        self.head = [0] * self.n
        self.position = [0] * self.n
        self.reverse_position = [0] * self.n
        self._current_position = 0

        self._dfs(0, -1)
        self._decompose(0, 0)
        ordered_values = [0] * self.n
        for node in range(self.n):
            ordered_values[self.position[node]] = self.values[node]
        self.segment_tree = RangeAddRangeSumSegmentTree(ordered_values)

    def _validate_node(self, node: int) -> None:
        if node < 0 or node >= self.n:
            raise IndexError(f"node {node} is outside the valid range 0..{self.n - 1}")

    def _dfs(self, node: int, parent: int) -> int:
        self.parent[node] = parent
        self.subtree_size[node] = 1
        largest_subtree = 0

        for neighbor in self.graph[node]:
            if neighbor == parent:
                continue

            self.depth[neighbor] = self.depth[node] + 1
            child_size = self._dfs(neighbor, node)
            self.subtree_size[node] += child_size

            if child_size > largest_subtree:
                largest_subtree = child_size
                self.heavy_child[node] = neighbor

        return self.subtree_size[node]

    def _decompose(self, node: int, chain_head: int) -> None:
        self.head[node] = chain_head
        self.position[node] = self._current_position
        self.reverse_position[self._current_position] = node
        self._current_position += 1

        heavy = self.heavy_child[node]
        if heavy != -1:
            self._decompose(heavy, chain_head)

        for neighbor in self.graph[node]:
            if neighbor != self.parent[node] and neighbor != heavy:
                self._decompose(neighbor, neighbor)

    def lca(self, left: int, right: int) -> int:
        self._validate_node(left)
        self._validate_node(right)

        while self.head[left] != self.head[right]:
            if self.depth[self.head[left]] > self.depth[self.head[right]]:
                left = self.parent[self.head[left]]
            else:
                right = self.parent[self.head[right]]

        return left if self.depth[left] < self.depth[right] else right

    def query_path(self, left: int, right: int) -> int:
        self._validate_node(left)
        self._validate_node(right)
        total = 0

        while self.head[left] != self.head[right]:
            if self.depth[self.head[left]] < self.depth[self.head[right]]:
                left, right = right, left

            chain_head = self.head[left]
            total += self.segment_tree.query(self.position[chain_head], self.position[left])
            left = self.parent[chain_head]

        if self.depth[left] > self.depth[right]:
            left, right = right, left

        total += self.segment_tree.query(self.position[left], self.position[right])
        return total

    def update_path(self, left: int, right: int, delta: int) -> None:
        self._validate_node(left)
        self._validate_node(right)

        while self.head[left] != self.head[right]:
            if self.depth[self.head[left]] < self.depth[self.head[right]]:
                left, right = right, left

            chain_head = self.head[left]
            self.segment_tree.add(self.position[chain_head], self.position[left], delta)
            left = self.parent[chain_head]

        if self.depth[left] > self.depth[right]:
            left, right = right, left

        self.segment_tree.add(self.position[left], self.position[right], delta)

    def query_node(self, node: int) -> int:
        self._validate_node(node)
        return self.segment_tree.query(self.position[node], self.position[node])

    def update_node(self, node: int, new_value: int) -> None:
        self._validate_node(node)
        current_value = self.query_node(node)
        self.segment_tree.add(self.position[node], self.position[node], new_value - current_value)

    def query_subtree(self, node: int) -> int:
        self._validate_node(node)
        left = self.position[node]
        right = left + self.subtree_size[node] - 1
        return self.segment_tree.query(left, right)

    def update_subtree(self, node: int, delta: int) -> None:
        self._validate_node(node)
        left = self.position[node]
        right = left + self.subtree_size[node] - 1
        self.segment_tree.add(left, right, delta)
