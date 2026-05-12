import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.hld import HeavyLightDecomposition


GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def header(text: str) -> None:
    print(f"\n{BOLD}{CYAN}{'=' * 60}{RESET}")
    print(f"{BOLD}{CYAN}  {text}{RESET}")
    print(f"{BOLD}{CYAN}{'=' * 60}{RESET}")


def section(text: str) -> None:
    print(f"\n{YELLOW}--- {text} ---{RESET}")


def ok(text: str) -> None:
    print(f"  {GREEN}✔ {text}{RESET}")


def build_sample_tree() -> HeavyLightDecomposition:
    edges = [
        (0, 1),
        (0, 2),
        (1, 3),
        (1, 4),
        (2, 5),
        (2, 6),
        (4, 7),
        (4, 8),
    ]
    values = [5, 3, 7, 2, 4, 6, 1, 8, 9]
    return HeavyLightDecomposition(9, edges, values)


def naive_path_sum(node_values, parents, left, right):
    left_path = []
    current = left
    while current != -1:
        left_path.append(current)
        current = parents[current]

    right_path = []
    current = right
    while current != -1:
        right_path.append(current)
        current = parents[current]

    left_set = set(left_path)
    lca = next(node for node in right_path if node in left_set)

    total = 0
    current = left
    while current != lca:
        total += node_values[current]
        current = parents[current]
    total += node_values[lca]

    stack = []
    current = right
    while current != lca:
        stack.append(current)
        current = parents[current]
    while stack:
        total += node_values[stack.pop()]
    return total


def main() -> None:
    header("HEAVY-LIGHT DECOMPOSITION DEMO")
    hld = build_sample_tree()
    node_values = [5, 3, 7, 2, 4, 6, 1, 8, 9]

    section("Path query from node 3 to node 6")
    path_sum = hld.query_path(3, 6)
    expected = naive_path_sum(node_values, hld.parent, 3, 6)
    ok(f"HLD path sum = {path_sum}")
    ok(f"Naive check  = {expected}")

    section("Apply path update +2 from node 3 to node 6")
    hld.update_path(3, 6, 2)
    for node in (3, 1, 0, 2, 6):
        node_values[node] += 2
    updated_path_sum = hld.query_path(3, 6)
    expected_after_update = naive_path_sum(node_values, hld.parent, 3, 6)
    ok(f"Updated path sum = {updated_path_sum}")
    ok(f"Naive check      = {expected_after_update}")

    section("Subtree query on node 4")
    subtree_sum = hld.query_subtree(4)
    expected_subtree = sum(node_values[node] for node in (4, 7, 8))
    ok(f"HLD subtree sum = {subtree_sum}")
    ok(f"Naive check      = {expected_subtree}")

    section("Point update on node 8")
    hld.update_node(8, 20)
    node_values[8] = 20
    ok(f"Node 8 value after update = {hld.query_node(8)}")
    ok(f"Total root-to-8 path sum   = {hld.query_path(0, 8)}")

    print(f"\n{BOLD}{GREEN}All demo checks completed successfully.{RESET}\n")


if __name__ == "__main__":
    main()
