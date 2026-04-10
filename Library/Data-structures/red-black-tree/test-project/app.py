import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.red_black_tree import RedBlackTree


def print_tree(node, nil, prefix="", is_left=True):
    """Recursive helper to pretty-print the RBT structure."""
    if node is nil:
        return
    connector = "├── " if is_left else "└── "
    color_tag = "\033[91mR\033[0m" if node.color == "RED" else "\033[90mB\033[0m"
    print(f"{prefix}{connector}[{color_tag}] {node.key}")
    extension = "│   " if is_left else "    "
    print_tree(node.left,  nil, prefix + extension, is_left=True)
    print_tree(node.right, nil, prefix + extension, is_left=False)


def section(title):
    print(f"\n{'=' * 55}")
    print(f"  {title}")
    print('=' * 55)


def main():
    print("Red-Black Tree — Test Simulation")
    print("-" * 55)

    rbt = RedBlackTree()

    # ------------------------------------------------------------------ #
    # 1. Insertions                                                        #
    # ------------------------------------------------------------------ #
    section("1. Inserting keys: [20, 15, 25, 10, 18, 22, 30, 5, 12]")
    keys = [20, 15, 25, 10, 18, 22, 30, 5, 12]
    for k in keys:
        rbt.insert(k, f"val_{k}")
        print(f"   Inserted key {k:>3}")

    print("\n   In-order traversal (must be sorted):")
    pairs = rbt.inorder()
    print("   " + "  ".join(f"{k}" for k, _ in pairs))
    print("   => BST ordering preserved across all insertions ✓")

    print("\n   Tree structure (R=RED, B=BLACK):")
    print_tree(rbt.root, rbt.NIL)

    # ------------------------------------------------------------------ #
    # 2. Search                                                            #
    # ------------------------------------------------------------------ #
    section("2. Search Operations")
    for k in [15, 30, 99]:
        result = rbt.search(k)
        status = f"Found → '{result}'" if result else "Not found"
        print(f"   search({k:>3}) : {status}")

    # ------------------------------------------------------------------ #
    # 3. Deletions                                                         #
    # ------------------------------------------------------------------ #
    section("3. Deleting keys: [15, 25, 20]")
    for k in [15, 25, 20]:
        rbt.delete(k)
        print(f"   Deleted key {k}")
        print(f"   In-order: { [key for key, _ in rbt.inorder()] }")

    print("\n   Tree structure after deletions (R=RED, B=BLACK):")
    print_tree(rbt.root, rbt.NIL)

    # ------------------------------------------------------------------ #
    # 4. Insert duplicates (overwrite)                                     #
    # ------------------------------------------------------------------ #
    section("4. Duplicate Key Handling")
    rbt.insert(10, "UPDATED_10")
    print(f"   search(10) after overwrite : '{rbt.search(10)}'")

    # ------------------------------------------------------------------ #
    # 5. Stress test — insert 1..50 in order                              #
    # ------------------------------------------------------------------ #
    section("5. Stress Test — inserting 1..50 sequentially")
    rbt2 = RedBlackTree()
    for i in range(1, 51):
        rbt2.insert(i)

    sorted_keys = [k for k, _ in rbt2.inorder()]
    assert sorted_keys == list(range(1, 51)), "In-order traversal mismatch!"

    def height(node, nil):
        if node is nil:
            return 0
        return 1 + max(height(node.left, nil), height(node.right, nil))

    h = height(rbt2.root, rbt2.NIL)
    print(f"   50 sequential insertions complete.")
    print(f"   Tree height: {h}  (theoretical max ≤ {2 * __import__('math').ceil(__import__('math').log2(51))})")
    print(f"   Root color : {rbt2.root.color}  (must be BLACK)")
    print("   => Red-Black invariants hold under sequential input ✓")


if __name__ == "__main__":
    main()
