import hashlib
import bisect

class ConsistentHashRing:
    """
    A simple Consistent Hashing ring implementation.
    """
    def __init__(self, replicas=3):
        self.replicas = replicas
        self.ring = dict()
        self.sorted_keys = []

    def _hash(self, key):
        """
        Returns a hash for a given key.
        Using MD5 for a good distribution, taking the first 8 bytes.
        """
        m = hashlib.md5()
        m.update(key.encode('utf-8'))
        return int(m.hexdigest()[:16], 16)

    def add_node(self, node):
        """
        Adds a node to the ring.
        Creates virtual nodes (replicas) to distribute the load evenly.
        """
        for i in range(self.replicas):
            replica_key = f"{node}:{i}"
            hashed_key = self._hash(replica_key)
            self.ring[hashed_key] = node
            bisect.insort(self.sorted_keys, hashed_key)

    def remove_node(self, node):
        """
        Removes a node and its virtual nodes from the ring.
        """
        for i in range(self.replicas):
            replica_key = f"{node}:{i}"
            hashed_key = self._hash(replica_key)
            if hashed_key in self.ring:
                del self.ring[hashed_key]
                self.sorted_keys.remove(hashed_key)

    def get_node(self, item):
        """
        Gets the node responsible for the given item.
        """
        if not self.ring:
            return None

        hashed_item = self._hash(item)
        
        # Find the first node with a hash greater than or equal to the item's hash
        idx = bisect.bisect(self.sorted_keys, hashed_item)
        
        # If the item's hash is greater than all nodes' hashes, wrap around to the first node
        if idx == len(self.sorted_keys):
            idx = 0
            
        return self.ring[self.sorted_keys[idx]]

if __name__ == "__main__":
    ring = ConsistentHashRing(replicas=3)
    ring.add_node("NodeA")
    ring.add_node("NodeB")
    ring.add_node("NodeC")

    print(f"Item 'apple' maps to: {ring.get_node('apple')}")
    print(f"Item 'banana' maps to: {ring.get_node('banana')}")
    print(f"Item 'cherry' maps to: {ring.get_node('cherry')}")
