# Running the Aho-Corasick Test App

This test project demonstrates the functionality of the Aho-Corasick Algorithm through a simple command-line interface. 

## Prerequisites
- Python 3.x installed.

## How to Run

1. Open a terminal or command prompt.
2. Navigate to the `test-project` directory of the Aho-Corasick algorithm:
   ```bash
   cd "Library/String-Algorithms/aho-corasick/test-project"
   ```
3. Run `app.py` using Python, providing a set of dictionary words and a search text.
   
### Usage Requirements
You need to pass two arguments:
- `--dict`: Followed by a space-separated list of words you want to search for.
- `--text`: The full string text in which to execute the search. (Enclose in quotes if it has spaces).

### Example Run

```bash
python app.py --dict he she his hers --text "ahishers"
```

### Expected Output

```
Initializing Aho-Corasick Automaton...
  Adding word: 'he'
  Adding word: 'she'
  Adding word: 'his'
  Adding word: 'hers'
Building failure links...

Searching within text: 'ahishers'
Found 4 matches:
  - 'his' found at index range [1...3]
  - 'she' found at index range [3...5]
  - 'he' found at index range [4...5]
  - 'hers' found at index range [4...7]
```
