class State:
    def __init__(self):
        self.length = 0
        self.link = -1
        self.next = {}

class SuffixAutomaton:
    """
    Suffix Automaton (Directed Acyclic Word Graph - DAWG)
    A powerful data structure that represents all substrings of a given string
    in a highly compressed form.
    """
    def __init__(self):
        self.states = [State()]
        self.sz = 1
        self.last = 0
        
    def extend(self, c: str):
        """
        Extends the automaton with a new character.
        """
        cur = self.sz
        self.sz += 1
        self.states.append(State())
        self.states[cur].length = self.states[self.last].length + 1
        
        p = self.last
        while p != -1 and c not in self.states[p].next:
            self.states[p].next[c] = cur
            p = self.states[p].link
            
        if p == -1:
            self.states[cur].link = 0
        else:
            q = self.states[p].next[c]
            if self.states[p].length + 1 == self.states[q].length:
                self.states[cur].link = q
            else:
                clone = self.sz
                self.sz += 1
                self.states.append(State())
                self.states[clone].length = self.states[p].length + 1
                self.states[clone].next = self.states[q].next.copy()
                self.states[clone].link = self.states[q].link
                
                while p != -1 and self.states[p].next.get(c) == q:
                    self.states[p].next[c] = clone
                    p = self.states[p].link
                    
                self.states[q].link = self.states[cur].link = clone
                
        self.last = cur

    def build(self, s: str):
        """
        Builds the automaton from a string.
        """
        for char in s:
            self.extend(char)

    def contains(self, string: str) -> bool:
        """
        Returns True if the string is a substring of the original string.
        """
        cur = 0
        for char in string:
            if char not in self.states[cur].next:
                return False
            cur = self.states[cur].next[char]
        return True
