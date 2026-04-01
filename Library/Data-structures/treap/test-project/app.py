import sys
import os

# Add parent directory to sys path in order to cleanly access Treap definitions
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.treap import Treap

def print_in_order(node):
    """Retrieve Tree keys and priorities via standard sorted indexing"""
    if not node:
        return []
    return print_in_order(node.left) + [(node.key, node.priority)] + print_in_order(node.right)

def main():
    print("Treap (Cartesian Tree) Test Simulation")
    print("-" * 45)
    
    treap = Treap()
    
    # 1. Insert Operations
    print("1. Inserting continuous sequence: [15, 10, 20, 5, 12, 18, 25]")
    for key in [15, 10, 20, 5, 12, 18, 25]:
        treap.insert(key, f"Value_{key}")
        
    print("\n   In-order Traversal Proof (Key, Priority):")
    for key, priority in print_in_order(treap.root):
        print(f"    Key: {key}, Priority: {priority:.4f}")
    print("\n   => Treap automatically retains perfectly incrementing Key indices regardless of randomized layout!")
    
    # 2. Search Results Test
    print("\n2. Launching lookup evaluations...")
    print(f"   Value queried at key 10: {treap.search(10)}")
    print(f"   Value queried at key 25: {treap.search(25)}")
    print(f"   Value queried at key 100 (non-existent): {treap.search(100)}")
    
    # 3. Dynamic Restructuring (Deletions)
    print("\n3. Testing recursive cleanup with targeted item omissions: [10, 20]")
    treap.delete(10)
    treap.delete(20)
    
    print(f"   Value queried at key 10 after deletion: {treap.search(10)}")
    
    print("\n   Post-Deletion Restructuring Results:")
    for key, priority in print_in_order(treap.root):
        print(f"    Key: {key}, Priority: {priority:.4f}")

if __name__ == "__main__":
    main()
