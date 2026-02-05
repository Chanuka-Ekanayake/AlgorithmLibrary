"""
Consistent Hashing Balancer
Implements a distributed hash ring with virtual nodes for horizontal scalability.
Ensures minimal data movement when scaling the server cluster.
"""

import hashlib
import bisect
from typing import List, Dict, Optional

class ConsistentHashRing:
    """
    Manages a distributed hash ring to map keys (requests/data) to nodes (servers).
    """

    def __init__(self, nodes: Optional[List[str]] = None, virtual_nodes: int = 100):
        """
        Args:
            nodes: Initial list of server identifiers (IPs or names).
            virtual_nodes: The number of virtual points per physical node.
                          Must be a positive integer. Higher values result in
                          more even distribution.
        """
        if not isinstance(virtual_nodes, int) or virtual_nodes <= 0:
            raise ValueError("virtual_nodes must be a positive integer")
        self.virtual_nodes = virtual_nodes
        self.ring: Dict[int, str] = {}      # Maps hash -> Physical Node Name
        self.sorted_keys: List[int] = []    # Sorted list of hashes for binary search
        
        if nodes:
            for node in nodes:
                self.add_node(node)

    def _hash(self, key: str) -> int:
        """
        Generates an MD5 hash for a string and converts it to an integer.
        MD5 is used here only for non-cryptographic purposes (consistent hashing)
        because of its speed and distribution properties. It is not used for, and
        is not suitable for, any security-sensitive functionality.
        """
        return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16)

    def add_node(self, node: str) -> None:
        """
        Adds a physical node to the ring by creating multiple virtual nodes.
        Complexity: O(V * log(N*V)) where V is virtual nodes.
        """
        for i in range(self.virtual_nodes):
            # Create a unique string for each virtual node
            v_node_name = f"{node}#vnode-{i}"
            v_hash = self._hash(v_node_name)
            
            self.ring[v_hash] = node
            # Maintain the sorted order for binary search (bisect_insort)
            bisect.insort(self.sorted_keys, v_hash)

    def remove_node(self, node: str) -> None:
        """
        Removes all virtual instances of a physical node from the ring.
        Useful for handling server decommission or failure.
        """
        for i in range(self.virtual_nodes):
            v_node_name = f"{node}#vnode-{i}"
            v_hash = self._hash(v_node_name)

            if v_hash in self.ring:
                del self.ring[v_hash]
                # Remove from sorted list (O(N) operation)
                if v_hash in self.sorted_keys:
                    self.sorted_keys.remove(v_hash)

    def get_node(self, request_key: str) -> Optional[str]:
        """
        Finds the correct physical node for a given request key.
        The request 'travels' clockwise on the ring until it hits a node.
        Complexity: O(log(N*V)) due to binary search.
        """
        if not self.sorted_keys:
            return None

        h = self._hash(request_key)
        
        # Find the index of the first node hash >= request hash
        idx = bisect.bisect_left(self.sorted_keys, h)
        
        # If we are past the last node, wrap around to the first node (the ring property)
        if idx == len(self.sorted_keys):
            idx = 0
            
        return self.ring[self.sorted_keys[idx]]

    def get_distribution_report(self) -> Dict[str, int]:
        """
        Utility for testing: Returns how many virtual slots each node occupies.
        """
        stats: Dict[str, int] = {}
        for node in self.ring.values():
            stats[node] = stats.get(node, 0) + 1
        return stats