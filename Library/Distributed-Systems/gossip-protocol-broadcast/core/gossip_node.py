"""
Gossip Protocol - Epidemic Broadcast Module
Implements a decentralized, eventually consistent communication protocol
using anti-entropy and rumor-mongering strategies.
"""

import random
from typing import Dict, List, Tuple, Any

class GossipNode:
    """
    A decentralized node that spreads information across a cluster 
    without a central leader.
    """

    def __init__(self, node_id: int, peer_ids: List[int]):
        """
        Args:
            node_id: Unique identifier for this node.
            peer_ids: List of identifiers for other nodes in the cluster.
        """
        self.node_id = node_id
        self.peer_ids = peer_ids
        
        # Knowledge Map: key -> (value, version_number)
        # Version numbers ensure we only accept the 'latest' rumor.
        self.knowledge: Dict[str, Tuple[Any, int]] = {}
        
        # Fan-out: How many peers to infect during each gossip cycle.
        self.fan_out = 2

    def inject_data(self, key: str, value: Any) -> None:
        """
        Manually inject or update data at this specific node.
        Increments the version to ensure it is treated as a 'new' rumor.
        """
        current_version = self.knowledge.get(key, (None, 0))[1]
        self.knowledge[key] = (value, current_version + 1)

    def select_gossip_targets(self) -> List[int]:
        """
        Randomly selects a subset of peers to spread information to.
        This is the 'epidemic' part of the algorithm.
        """
        if not self.peer_ids:
            return []
        
        return random.sample(
            self.peer_ids, 
            min(len(self.peer_ids), self.fan_out)
        )

    def prepare_gossip_payload(self) -> Dict[str, Tuple[Any, int]]:
        """
        Returns the node's current knowledge to be sent to peers.
        In a production system, this might be compressed or delta-encoded.
        """
        return self.knowledge

    def receive_gossip(self, incoming_knowledge: Dict[str, Tuple[Any, int]]) -> bool:
        """
        Processes incoming rumors from a peer.
        Uses 'Anti-Entropy' to resolve conflicts: the higher version always wins.
        Returns: True if new information was learned.
        """
        updated = False
        for key, (val, ver) in incoming_knowledge.items():
            _, current_ver = self.knowledge.get(key, (None, 0))
            
            if ver > current_ver:
                self.knowledge[key] = (val, ver)
                updated = True
        return updated

    def get_value(self, key: str) -> Any:
        """Retrieves the value for a key if it exists."""
        entry = self.knowledge.get(key)
        return entry[0] if entry else None

    def __repr__(self):
        return f"<GossipNode {self.node_id}: {len(self.knowledge)} items>"