class SuffixTreeNode:
    def __init__(self, start, end):
        self.children = {}
        self.start = start
        self.end = end
        self.suffix_link = None

    def length(self, current_end):
        return min(self.end[0], current_end) - self.start + 1

class SuffixTree:
    def __init__(self, text):
        if "$" in text:
            raise ValueError("Input text for SuffixTree must not contain the terminator character '$'.")
        self.text = text + "$"
        self.n = len(self.text)
        self.root = SuffixTreeNode(-1, [-1])
        self.active_node = self.root
        self.active_edge = -1
        self.active_len = 0
        self.remaining = 0
        self.current_end = [-1]
        
        for i in range(self.n):
            self._extend(i)

    def _extend(self, pos):
        self.current_end[0] += 1
        self.remaining += 1
        last_created_internal_node = None

        while self.remaining > 0:
            if self.active_len == 0:
                self.active_edge = pos

            char = self.text[self.active_edge]
            if char not in self.active_node.children:
                # Rule 2: Create new leaf
                self.active_node.children[char] = SuffixTreeNode(pos, self.current_end)
                if last_created_internal_node:
                    last_created_internal_node.suffix_link = self.active_node
                    last_created_internal_node = None
            else:
                next_node = self.active_node.children[char]
                edge_len = next_node.length(self.current_end[0])
                
                # Observation 1: Skip/Count trick (walk down)
                if self.active_len >= edge_len:
                    self.active_edge += edge_len
                    self.active_len -= edge_len
                    self.active_node = next_node
                    continue

                # Rule 3: Character found on edge
                if self.text[next_node.start + self.active_len] == self.text[pos]:
                    if last_created_internal_node and self.active_node != self.root:
                        last_created_internal_node.suffix_link = self.active_node
                    self.active_len += 1
                    break  # Stop extension for this phase

                # Rule 2: Split edge
                split_end = [next_node.start + self.active_len - 1]
                split_node = SuffixTreeNode(next_node.start, split_end)
                self.active_node.children[char] = split_node
                
                # New leaf from split
                split_node.children[self.text[pos]] = SuffixTreeNode(pos, self.current_end)
                
                # Redirect old child
                next_node.start += self.active_len
                split_node.children[self.text[next_node.start]] = next_node
                
                if last_created_internal_node:
                    last_created_internal_node.suffix_link = split_node
                
                last_created_internal_node = split_node

            self.remaining -= 1
            if self.active_node == self.root and self.active_len > 0:
                self.active_len -= 1
                self.active_edge = pos - self.remaining + 1
            elif self.active_node != self.root:
                self.active_node = self.active_node.suffix_link if self.active_node.suffix_link else self.root

    def search(self, pattern):
        # Reject patterns containing the reserved terminator, which is only used
        # internally to build the augmented text for the suffix tree.
        if "$" in pattern:
            return False

        curr = self.root
        i = 0
        while i < len(pattern):
            char = pattern[i]
            if char not in curr.children:
                return False
            
            node = curr.children[char]
            edge_len = node.length(self.current_end[0])
            j = 0
            while j < edge_len and i < len(pattern):
                if self.text[node.start + j] != pattern[i]:
                    return False
                i += 1
                j += 1
            curr = node
        return True

    def find_all(self, pattern):
        # Reject patterns containing the reserved terminator, which is only used
        # internally to build the augmented text for the suffix tree.
        if "$" in pattern:
            return []

        # Find node representing the pattern
        curr = self.root
        i = 0
        while i < len(pattern):
            char = pattern[i]
            if char not in curr.children:
                return []
            
            node = curr.children[char]
            edge_len = node.length(self.current_end[0])
            j = 0
            while j < edge_len and i < len(pattern):
                if self.text[node.start + j] != pattern[i]:
                    return []
                i += 1
                j += 1
            curr = node
        
        # Collect all leaf indices under this node
        results = []
        self._collect_leaf_indices(curr, results)
        return sorted(results)

    def _collect_leaf_indices(self, node, results):
        if not node.children:
            # Reconstruct the index. Since each leaf represents a suffix, 
            # we need to calculate where it starts.
            # In Ukkonen's, leaf index is often best tracked by adding it to the node
            # during construction. For simplicity in this implementation, we calculate:
            results.append(len(self.text) - self._get_depth(node))
            return

        for child in node.children.values():
            self._collect_leaf_indices(child, results)

    def _get_depth(self, node):
        """
        Compute the depth (in characters) from the root to the given node.

        The depth is the total length of all edge labels on the path from the
        root to `node`. This is used by `_collect_leaf_indices` to reconstruct
        the starting index of the suffix represented by a leaf:

            suffix_start = len(self.text) - depth
        """
        target = node

        def _dfs(current, depth):
            # If we've reached the target node, return the accumulated depth.
            if current is target:
                return depth

            # Explore children, accumulating edge lengths.
            for child in current.children.values():
                edge_len = child.length(self.current_end[0])
                found_depth = _dfs(child, depth + edge_len)
                if found_depth is not None:
                    return found_depth

            return None

        result = _dfs(self.root, 0)
        if result is None:
            # This should not happen for nodes that are part of the tree.
            raise ValueError("Node is not reachable from the root")
        return result
