from typing import Dict, List, Optional

class TrieNode:
    """A node in the Trie. Each node represents a single character."""
    def __init__(self):
        # Dictionary to store children: {char: TrieNode}
        self.children: Dict[str, TrieNode] = {}
        # Flag to indicate if this character is the end of a valid word
        self.is_end_of_word: bool = False

class Trie:
    """
    Trie (Prefix Tree) implementation for efficient string prefix searching.
    Ideal for search engines and auto-complete systems.
    """
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """
        Inserts a word into the Trie.
        Time Complexity: O(L) where L is the length of the word.
        """
        node = self.root
        for char in word.lower():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search_prefix(self, prefix: str) -> Optional[TrieNode]:
        """
        Finds the node representing the end of the given prefix.
        Returns None if prefix doesn't exist.
        """
        node = self.root
        for char in prefix.lower():
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def get_words_with_prefix(self, prefix: str) -> List[str]:
        """
        Finds all words in the Trie that start with the given prefix.
        """
        node = self.search_prefix(prefix)
        if not node:
            return []

        results = []
        self._dfs_collect(node, prefix.lower(), results)
        return results

    def _dfs_collect(self, node: TrieNode, current_prefix: str, results: List[str]):
        """Depth First Search helper to find all words under a node."""
        if node.is_end_of_word:
            results.append(current_prefix)

        for char, next_node in node.children.items():
            self._dfs_collect(next_node, current_prefix + char, results)