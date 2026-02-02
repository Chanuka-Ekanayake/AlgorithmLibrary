"""
Huffman Coding Engine
Implements lossless data compression using a greedy frequency-based tree.
Used for optimizing data storage and transmission bandwidth.
"""

import heapq
from collections import Counter
from typing import Dict, Optional, Tuple

class HuffmanNode:
    """
    A node in the Huffman Tree.
    """
    def __init__(self, char: Optional[str], freq: int):
        self.char = char
        self.freq = freq
        self.left: Optional['HuffmanNode'] = None
        self.right: Optional['HuffmanNode'] = None

    def __lt__(self, other: 'HuffmanNode') -> bool:
        """Comparison for priority queue (min-heap)."""
        return self.freq < other.freq

class HuffmanCoder:
    """
    Engine for encoding and decoding text using Huffman compression.
    """
    def __init__(self):
        self.encoder: Dict[str, str] = {}
        self.decoder: Dict[str, str] = {}

    def _build_tree(self, text: str) -> Optional[HuffmanNode]:
        """Builds the optimal binary tree based on character frequencies."""
        if not text:
            return None

        # 1. Count frequencies
        frequencies = Counter(text)
        
        # 2. Build min-heap of leaf nodes
        priority_queue = [HuffmanNode(char, freq) for char, freq in frequencies.items()]
        heapq.heapify(priority_queue)

        # 3. Iterate until tree is complete (Greedy Strategy)
        while len(priority_queue) > 1:
            node1 = heapq.heappop(priority_queue)
            node2 = heapq.heappop(priority_queue)

            # Create internal node with combined frequency
            merged = HuffmanNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2
            heapq.heappush(priority_queue, merged)

        return heapq.heappop(priority_queue)

    def _generate_codes(self, node: Optional[HuffmanNode], current_code: str):
        """Recursively generates binary strings for each character."""
        if node is None:
            return

        # Found a leaf node (actual character)
        if node.char is not None:
            self.encoder[node.char] = current_code
            self.decoder[current_code] = node.char
            return

        self._generate_codes(node.left, current_code + "0")
        self._generate_codes(node.right, current_code + "1")

    def compress(self, text: str) -> Tuple[str, float]:
        """
        Compresses input text into a bitstring.
        Returns: (bitstring, compression_ratio)
        """
        if not text:
            return "", 0.0

        # Reset mappings for new text
        self.encoder = {}
        self.decoder = {}

        root = self._build_tree(text)
        self._generate_codes(root, "")

        bitstring = "".join([self.encoder[char] for char in text])
        
        # Calculate ratio: (Compressed Size in bits) / (Original Size in 8-bit characters)
        original_size_bits = len(text) * 8
        compressed_size_bits = len(bitstring)
        ratio = 1 - (compressed_size_bits / original_size_bits)

        return bitstring, ratio

    def decompress(self, bitstring: str) -> str:
        """Decompresses a bitstring back into the original text."""
        current_code = ""
        decoded_chars = []

        for bit in bitstring:
            current_code += bit
            if current_code in self.decoder:
                decoded_chars.append(self.decoder[current_code])
                current_code = ""

        return "".join(decoded_chars)