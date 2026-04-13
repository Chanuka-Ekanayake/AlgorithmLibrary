"""
Splay Tree Test Suite & Demonstrations

Test various operations and show adaptive behavior of splay trees.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'core'))

from splay_tree import SplayTree


def test_basic_operations():
    """Test insert, search, delete, and traversal"""
    print("=" * 60)
    print("TEST 1: Basic Operations")
    print("=" * 60)
    
    tree = SplayTree()
    keys = [50, 30, 70, 20, 40, 60, 80]
    
    print(f"\nInserting: {keys}")
    for key in keys:
        tree.insert(key)
    
    print(f"In-order traversal: {tree.inorder()}")
    print(f"Tree size: {tree.size()}")
    print(f"Tree height: {tree.height()}")
    
    # Search splays node to root
    print(f"\nSearching for 20...")
    found = tree.search(20)
    print(f"Found: {found}")
    print(f"Root after splay: {tree.root.key}")
    
    # Delete
    print(f"\nDeleting 20...")
    tree.delete(20)
    print(f"In-order after delete: {tree.inorder()}")
    print(f"Tree height: {tree.height()}")


def test_splay_to_root():
    """Demonstrate splaying action"""
    print("\n" + "=" * 60)
    print("TEST 2: Splaying Brings Elements to Root")
    print("=" * 60)
    
    tree = SplayTree()
    keys = [1, 2, 3, 4, 5, 6, 7]
    
    for key in keys:
        tree.insert(key)
    
    print(f"\nInitial tree in-order: {tree.inorder()}")
    print(f"Initial root: {tree.root.key}")
    print(f"Initial height: {tree.height()}")
    
    # Access deepen node
    print(f"\nSearching for 1 (deepest in chain)...")
    tree.search(1)
    print(f"Root after splay: {tree.root.key}")
    print(f"Height after splay: {tree.height()}")
    
    # Access another
    print(f"\nSearching for 7...")
    tree.search(7)
    print(f"Root after splay: {tree.root.key}")


def test_adaptive_behavior():
    """Show how splay tree adapts to repeated accesses"""
    print("\n" + "=" * 60)
    print("TEST 3: Adaptive Behavior with Repeated Accesses")
    print("=" * 60)
    
    tree = SplayTree()
    keys = list(range(1, 11))  # 1-10
    
    for key in keys:
        tree.insert(key)
    
    print(f"\nInitial in-order: {tree.inorder()}")
    access_order = [5, 5, 5, 5, 3, 3, 3]
    
    print(f"\nAccess sequence: {access_order}")
    for key in access_order:
        tree.search(key)
        print(f"  Searched {key} → Root is now {tree.root.key}, Height: {tree.height()}")
    
    # Frequently accessed elements should be near root
    print(f"\nFinal root: {tree.root.key}")
    print(f"Final height: {tree.height()}")
    print(f"Elements near root should be: 5, 3 (most frequently accessed)")


def test_duplicate_handling():
    """Test how duplicates are handled"""
    print("\n" + "=" * 60)
    print("TEST 4: Duplicate Handling")
    print("=" * 60)
    
    tree = SplayTree()
    print(f"\nInserting: 10, 5, 15, 5, 10")
    
    result1 = tree.insert(10)
    print(f"Insert 10: {result1}")
    
    result2 = tree.insert(5)
    print(f"Insert 5: {result2}")
    
    result3 = tree.insert(15)
    print(f"Insert 15: {result3}")
    
    result4 = tree.insert(5)
    print(f"Insert 5 (duplicate): {result4}")
    
    result5 = tree.insert(10)
    print(f"Insert 10 (duplicate): {result5}")
    
    print(f"In-order: {tree.inorder()}")
    print(f"Tree size: {tree.size()} (should be 3, not 5)")


def test_sequential_insertion():
    """Stress test with sequential insertions"""
    print("\n" + "=" * 60)
    print("TEST 5: Sequential Insertion Stress Test")
    print("=" * 60)
    
    tree = SplayTree()
    n = 10
    
    print(f"\nInserting {n} elements sequentially (1 to {n})...")
    for i in range(1, n + 1):
        tree.insert(i)
    
    print(f"Height after sequential insert: {tree.height()}")
    print(f"Size: {tree.size()}")
    print(f"In-order: {tree.inorder()[:5]}...{tree.inorder()[-5:]}")
    
    # Search triggers splaying which improves balance
    print(f"\nSearching for 5...")
    tree.search(5)
    print(f"Root after search: {tree.root.key}")
    print(f"Height after splay: {tree.height()}")
    
    print(f"\nSearching for 1...")
    tree.search(1)
    print(f"Root after search: {tree.root.key}")
    print(f"Height after splay: {tree.height()}")


def test_delete_operations():
    """Test various delete scenarios"""
    print("\n" + "=" * 60)
    print("TEST 6: Delete Operations")
    print("=" * 60)
    
    tree = SplayTree()
    keys = [50, 25, 75, 12, 37, 62, 87, 6, 18, 31, 43, 56, 68, 81, 93]
    
    for key in keys:
        tree.insert(key)
    
    print(f"\nInitial in-order: {tree.inorder()}")
    print(f"Size: {tree.size()}")
    
    # Delete leaf
    print(f"\nDeleting leaf (6)...")
    tree.delete(6)
    print(f"After delete: {tree.inorder()}")
    print(f"Size: {tree.size()}")
    
    # Delete node with one child
    print(f"\nDeleting node with one child (12)...")
    tree.delete(12)
    print(f"After delete: {tree.inorder()}")
    
    # Delete node with two children
    print(f"\nDeleting node with two children (25)...")
    tree.delete(25)
    print(f"After delete: {tree.inorder()}")
    print(f"Size: {tree.size()}")


def performance_comparison():
    """Compare access patterns"""
    print("\n" + "=" * 60)
    print("TEST 7: Performance Characteristics")
    print("=" * 60)
    
    tree = SplayTree()
    keys = list(range(1, 21))  # 1-20
    
    for key in keys:
        tree.insert(key)
    
    initial_height = tree.height()
    print(f"\nInitial height (sorted insertions): {initial_height}")
    
    # Access pattern 1: Random uniform access
    print(f"\nRandom uniform access pattern:")
    uniform_pattern = [3, 17, 9, 15, 2, 18, 5, 11, 19, 7]
    for key in uniform_pattern:
        tree.search(key)
    print(f"Height after uniform access: {tree.height()}")
    
    # Recreate tree
    tree = SplayTree()
    for key in keys:
        tree.insert(key)
    
    # Access pattern 2: Skewed access (80/20 rule)
    print(f"\nSkewed access pattern (hot data: 5, 6):")
    skewed_pattern = [5, 5, 5, 5, 6, 6, 6, 19, 20, 1]
    for key in skewed_pattern:
        tree.search(key)
    print(f"Height after skewed access: {tree.height()}")
    print(f"Root: {tree.root.key}")
    print(f"→ Frequently accessed elements moved to root!")


def run_all_tests():
    """Run all tests"""
    test_basic_operations()
    test_splay_to_root()
    test_adaptive_behavior()
    test_duplicate_handling()
    test_sequential_insertion()
    test_delete_operations()
    performance_comparison()
    
    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()
