import argparse

# Adjusting import path assuming execution might happen correctly if relative logic works, 
# but simply bringing the class locally or running as module is safer. Here we assume we can import it.
import sys
import os

# Add the core directory to sys.path to allow easy importing
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'core')))

try:
    from aho_corasick import AhoCorasick
except ImportError:
    print(
        "Error: Could not import AhoCorasick from the core module. "
        "Ensure 'core/aho_corasick.py' exists and is accessible from this test project."
    )
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Test project for Aho-Corasick Algorithm")
    parser.add_argument(
        "--dict", 
        nargs="+", 
        required=True, 
        help="List of words to include in the dictionary."
    )
    parser.add_argument(
        "--text", 
        type=str, 
        required=True, 
        help="The text string to search the dictionary words within."
    )
    
    args = parser.parse_args()
    
    print("Initializing Aho-Corasick Automaton...")
    ac = AhoCorasick()
    
    # Add words
    for word in args.dict:
        print(f"  Adding word: '{word}'")
        ac.add_word(word)
        
    print("Building failure links...")
    ac.build()
    
    print(f"\nSearching within text: '{args.text}'")
    results = ac.search(args.text)
    
    if not results:
        print("No matches found.")
    else:
        print(f"Found {len(results)} matches:")
        for end_idx, word in results:
            start_idx = end_idx - len(word) + 1
            print(f"  - '{word}' found at index range [{start_idx}...{end_idx}]")

if __name__ == "__main__":
    main()
