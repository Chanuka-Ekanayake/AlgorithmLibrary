import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.suffix_automaton import SuffixAutomaton

class TestSuffixAutomaton(unittest.TestCase):
    def test_substrings(self):
        sa = SuffixAutomaton()
        sa.build("automaton")
        
        self.assertTrue(sa.contains("auto"))
        self.assertTrue(sa.contains("maton"))
        self.assertTrue(sa.contains("toma"))
        self.assertTrue(sa.contains("o"))
        self.assertTrue(sa.contains("automaton"))
        
        self.assertFalse(sa.contains("autz"))
        self.assertFalse(sa.contains("tomatos"))
        self.assertFalse(sa.contains("automatons"))
        self.assertFalse(sa.contains("z"))

if __name__ == '__main__':
    unittest.main()
