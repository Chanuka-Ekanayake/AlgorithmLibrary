import sys
import os

# Add parent directory to path for core logic access
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.rabin_karp import RabinKarp

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_signatures(filepath):
    """Loads malicious patterns from a text file."""
    try:
        with open(filepath, 'r') as f:
            # Return non-empty lines as patterns
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Error loading signatures: {e}")
        return []

def run_malware_scan():
    clear_screen()
    print("--------------------------------------------------")
    print("SYSTEM: SECURE-MARKETPLACE MALWARE SCANNER")
    print("ALGORITHM: RABIN-KARP MULTI-PATTERN MATCHING")
    print("--------------------------------------------------\n")

    # 1. Initialize Engine and Load Data
    scanner = RabinKarp()
    signatures = load_signatures('library.txt')
    
    # Simulating a suspicious file content
    target_file_content = """
    import os
    import sys
    
    def initialize_app():
        print("App starting...")
        # Security vulnerability below
        os.system('chmod 777 /etc/shadow') 
        print("App ready.")
        
    if __name__ == "__main__":
        initialize_app()
    """

    print(f"LOADED: {len(signatures)} known malicious signatures.")
    print("SCANNING: Suspicious Python Script...")
    print("--------------------------------------------------\n")

    # 2. Perform Batch Search
    found_threats = scanner.batch_search(signatures, target_file_content)

    # 3. Output Results
    if found_threats:
        print("🔴 ALERT: MALICIOUS CONTENT DETECTED!")
        print("--------------------------------------------------")
        for signature, indices in found_threats.items():
            for idx in indices:
                print(f"THREAT FOUND: '{signature}'")
                print(f"LOCATION:     Index {idx}")
                print(f"CONTEXT:      ...{target_file_content[idx:idx+30]}...")
                print("-" * 30)
    else:
        print("🟢 CLEAN: No malicious signatures found in the file.")

    print("\n--------------------------------------------------")
    print("SCAN COMPLETE")
    print("--------------------------------------------------")

if __name__ == "__main__":
    run_malware_scan()