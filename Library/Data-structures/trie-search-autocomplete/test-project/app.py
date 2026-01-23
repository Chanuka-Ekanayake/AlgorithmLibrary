import sys
import os

# Add the parent directory to the path so we can import the core logic
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.trie import Trie

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def marketplace_search_simulation():
    clear_screen()
    engine = Trie()
    
    # Pre-populate with some "Trending 2026" ML Models
    initial_models = [
        "transformer-vision", "transformer-text", "stable-diffusion-v5",
        "llama-7b-quantized", "linear-regression-pro", "logistic-bottleneck"
    ]
    for model in initial_models:
        engine.insert(model)

    print("==================================================")
    print("E-COMMERCE SEARCH ENGINE: TRIE AUTOCOMPLETE ")
    print("==================================================\n")
    
    print("SCENARIO: You are building the search bar for an ML Model Marketplace.")
    print("Users expect instant suggestions as they type their queries.\n")

    while True:
        print("\n--- MAIN MENU ---")
        print("1. Search / Autocomplete")
        print("2. Add New Product to Catalog")
        print("3. View Catalog Recommendations")
        print("4. Exit")
        
        choice = input("\nSelect an option (1-4): ").strip()

        if choice == '1':
            print("\n--- 🔍 LIVE SEARCH SIMULATOR ---")
            query = input("Start typing a model name: ").strip().lower()
            
            # Logic: Get all words that start with the input prefix
            suggestions = engine.get_words_with_prefix(query)
            
            if suggestions:
                print(f"\n✨ {len(suggestions)} Suggestions Found:")
                for i, s in enumerate(suggestions, 1):
                    print(f"   {i}. {s}")
            else:
                print(f"\nNo models found starting with '{query}'.")

        elif choice == '2':
            new_item = input("\nEnter the name of the new ML model/software: ").strip().lower()
            if new_item:
                engine.insert(new_item)
                print(f" '{new_item}' has been indexed into the Trie!")

        elif choice == '3':
            # This demonstrates how Tries can handle empty prefixes to show all content
            all_models = engine.get_words_with_prefix("")
            print(f"\nCURRENT CATALOG ({len(all_models)} items):")
            print(", ".join(all_models))

        elif choice == '4':
            print("\nShutting down Search Engine... Goodbye!")
            break
        
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    marketplace_search_simulation()