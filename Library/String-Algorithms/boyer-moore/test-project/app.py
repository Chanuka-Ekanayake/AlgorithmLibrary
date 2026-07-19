import sys
import os

# Add the parent directory of 'core' to the python path so we can import it
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.boyer_moore import search

def main():
    print("=== Boyer-Moore String Search Algorithm ===")
    
    text = input("Enter the text to search in: ")
    pattern = input("Enter the pattern to search for: ")
    
    if not text or not pattern:
        print("Text or pattern cannot be empty.")
        return
        
    occurrences = search(text, pattern)
    
    print("\n--- Results ---")
    if occurrences:
        print(f"Pattern '{pattern}' found {len(occurrences)} time(s) at index/indices:")
        print(occurrences)
        
        # Display visual aid for the first occurrence
        first_idx = occurrences[0]
        print("\nVisual alignment of the first occurrence:")
        print("Text:    ", text)
        print("Pattern: " + " " * first_idx + pattern)
    else:
        print(f"Pattern '{pattern}' not found in the text.")

if __name__ == "__main__":
    main()
