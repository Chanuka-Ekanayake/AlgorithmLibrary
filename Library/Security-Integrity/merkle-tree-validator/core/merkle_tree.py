"""
Merkle Tree Integrity Validator
Implements a cryptographic Hash Tree for efficient and secure data verification.
Ideal for verifying large software binaries or ML model weights.
"""

import hashlib
from typing import List, Optional, Tuple

class MerkleTree:
    """
    A Merkle Tree implementation using SHA-256.
    Provides Root Hash generation and Merkle Proofs for leaf verification.
    """
    def __init__(self, data_blocks: List[str]):
        if not data_blocks:
            raise ValueError("Data blocks cannot be empty.")
            
        # Store original data and their initial hashes (Leaf Nodes)
        self.data_blocks = data_blocks
        self.levels: List[List[str]] = []
        self._build_tree()

    def _hash(self, data: str) -> str:
        """Standard SHA-256 hashing."""
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    def _build_tree(self) -> None:
        """Builds the tree from leaves to root."""
        # Level 0 is the hash of each data block
        current_level = [self._hash(block) for block in self.data_blocks]
        self.levels.append(current_level)

        while len(current_level) > 1:
            next_level = []
            # Process nodes in pairs
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                # If odd number of nodes, the last node is paired with itself
                right = current_level[i + 1] if i + 1 < len(current_level) else current_level[i]
                
                combined_hash = self._hash(left + right)
                next_level.append(combined_hash)
            
            self.levels.append(next_level)
            current_level = next_level

    def get_root_hash(self) -> str:
        """Returns the top-level hash (The Digital Fingerprint)."""
        return self.levels[-1][0]

    def get_proof(self, index: int) -> List[Tuple[str, str]]:
        """
        Generates a Merkle Proof for the data block at the given index.
        A proof is a list of (hash, direction) tuples needed to reconstruct the root.
        """
        if index < 0 or index >= len(self.data_blocks):
            raise IndexError("Data block index out of range.")

        proof = []
        current_index = index

        # Traverse up the tree, excluding the root level
        for level in self.levels[:-1]:
            # Determine the sibling's index
            is_right_node = current_index % 2 == 1
            sibling_index = current_index - 1 if is_right_node else current_index + 1
            
            # If the index is out of bounds (odd node at end), the sibling is itself
            if sibling_index < len(level):
                direction = "left" if is_right_node else "right"
                proof.append((level[sibling_index], direction))
            
            current_index //= 2
            
        return proof

    @staticmethod
    def verify_proof(target_data: str, proof: List[Tuple[str, str]], root_hash: str) -> bool:
        """
        Verifies if target_data belongs to a tree with the given root_hash using the proof.
        This is the O(log n) verification step.
        """
        def sha256_hash(data: str) -> str:
            return hashlib.sha256(data.encode('utf-8')).hexdigest()

        current_hash = sha256_hash(target_data)

        for sibling_hash, direction in proof:
            if direction == "left":
                current_hash = sha256_hash(sibling_hash + current_hash)
            else:
                current_hash = sha256_hash(current_hash + sibling_hash)

        return current_hash == root_hash