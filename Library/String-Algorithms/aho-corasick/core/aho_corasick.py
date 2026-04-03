from collections import deque

class AhoCorasick:
    def __init__(self):
        # Trie is represented as a list of dictionaries (states)
        self.transitions = [{}] 
        # failure_link[i] will store the failure link for state i
        self.failure_links = [0]
        # output[i] stores the list of word indices that end at state i 
        self.output = [[]]
        self.words = []

    def add_word(self, word):
        """Add a word to the Aho-Corasick Automaton."""
        current_state = 0
        for char in word:
            if char not in self.transitions[current_state]:
                # Create a new state
                self.transitions[current_state][char] = len(self.transitions)
                self.transitions.append({})
                self.failure_links.append(0)
                self.output.append([])
            current_state = self.transitions[current_state][char]
        
        self.output[current_state].append(len(self.words))
        self.words.append(word)

    def build(self):
        """Construct the failure links and dictionary links utilizing BFS."""
        # Queue for BFS
        queue = deque()
        
        # Initialize the depth 1 nodes failure links to 0 (root)
        for char, next_state in self.transitions[0].items():
            self.failure_links[next_state] = 0
            queue.append(next_state)
            
        while queue:
            current_state = queue.popleft()
            
            for char, next_state in self.transitions[current_state].items():
                queue.append(next_state)
                
                # Follow failure links to find the longest strict suffix
                fail_state = self.failure_links[current_state]
                while fail_state != 0 and char not in self.transitions[fail_state]:
                    fail_state = self.failure_links[fail_state]
                    
                if char in self.transitions[fail_state]:
                    fail_state = self.transitions[fail_state][char]
                else:
                    fail_state = 0
                    
                self.failure_links[next_state] = fail_state
                
                # Merge outputs of the fail state to current state to handle dictionary links implicitly
                self.output[next_state].extend(self.output[fail_state])

    def search(self, text):
        """
        Search for all occurrences of the added words in the text.
        Returns a list of tuples: (end_index, matched_word)
        """
        current_state = 0
        results = []
        
        for i, char in enumerate(text):
            while current_state != 0 and char not in self.transitions[current_state]:
                current_state = self.failure_links[current_state]
                
            if char in self.transitions[current_state]:
                current_state = self.transitions[current_state][char]
            else:
                current_state = 0
                
            for word_index in self.output[current_state]:
                results.append((i, self.words[word_index]))
                
        return results

if __name__ == "__main__":
    ac = AhoCorasick()
    words_to_add = ["he", "she", "his", "hers"]
    for w in words_to_add:
        ac.add_word(w)
        
    ac.build()
    
    match_results = ac.search("ahishers")
    for end_idx, word in match_results:
        print(f"Matched '{word}' ending at index {end_idx}")
