import sys
import io
import time
from pathlib import Path

# Fix Windows console encoding for Unicode output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Add parent directory to path for core logic access
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

try:
    from core.sha256 import sha256
except ImportError:
    print("Error: Ensure 'core/sha256.py' and 'core/__init__.py' exist.")
    sys.exit(1)


def highlight_diff(hash1, hash2):
    """Helper to visualize identical vs different characters in two hashes."""
    result = ""
    diff_count = 0
    for c1, c2 in zip(hash1, hash2):
        if c1 == c2:
            result += c1
        else:
            result += f"\033[91m{c2}\033[0m"  # Red for differences (if terminal supports ANSI)
            diff_count += 1
    return diff_count

def run_avalanche_demo():
    print("\n" + "=" * 65)
    print("  SHA-256 DEMO 1: THE AVALANCHE EFFECT")
    print("=" * 65)
    print("  A cryptographic hash function must exhibit the Avalanche Effect:")
    print("  Changing a single bit in the input should completely and")
    print("  unpredictably change the output hash.")
    print("-" * 65)

    base_string = "The quick brown fox jumps over the lazy dog"
    print(f"  Base Input: '{base_string}'")
    
    hash_base = sha256(base_string)
    print(f"  Base Hash:   {hash_base}\n")
    
    # Change a single letter
    mod_string1 = "The quick brown fox jumps over the lazy cog"
    print(f"  Mod Input 1: '{mod_string1}' (Changed 'd' to 'c')")
    hash_mod1 = sha256(mod_string1)
    print(f"  Mod Hash 1:  {hash_mod1}\n")
    
    # Change capitalization
    mod_string2 = "the quick brown fox jumps over the lazy dog"
    print(f"  Mod Input 2: '{mod_string2}' (Changed 'T' to 't')")
    hash_mod2 = sha256(mod_string2)
    print(f"  Mod Hash 2:  {hash_mod2}\n")

    # Add a period
    mod_string3 = "The quick brown fox jumps over the lazy dog."
    print(f"  Mod Input 3: '{mod_string3}' (Added a period)")
    hash_mod3 = sha256(mod_string3)
    print(f"  Mod Hash 3:  {hash_mod3}\n")


def run_proof_of_work_demo():
    print("=" * 65)
    print("  SHA-256 DEMO 2: PROOF-OF-WORK (BITCOIN MINER SIMULATOR)")
    print("=" * 65)
    print("  Bitcoin mining involves rapidly changing a 'nonce' value until")
    print("  the resulting SHA-256 hash starts with a specific number of zeros.")
    print("  Because hashing is unpredictable, this requires brute-force.")
    print("-" * 65)

    block_data = "Transaction: Alice pays Bob $100 | Nonce: "
    target_leading_zeros = 3
    target_prefix = "0" * target_leading_zeros
    
    print(f"  Target: Find a hash starting with {target_leading_zeros} zeros ('{target_prefix}')")
    print(f"  Data: '{block_data} [X]'\n")
    
    nonce = 0
    start_time = time.time()
    
    while True:
        # Create the string to hash
        data_to_hash = block_data + str(nonce)
        
        # Calculate SHA-256
        current_hash = sha256(data_to_hash)
        
        # Print a sample of the attempts to the console to show it working
        if nonce % 500 == 0:
            print(f"  Attempt {nonce:4d}: {current_hash} (No match)")
            
        # Check if it meets the criteria
        if current_hash.startswith(target_prefix):
            elapsed = time.time() - start_time
            print("-" * 65)
            print(f"  [SUCCESS] Block successfully mined!")
            print(f"  Nonce found: {nonce}")
            print(f"  Valid Hash:  {current_hash}")
            print(f"  Time taken:  {elapsed:.2f} seconds ({nonce/elapsed:.0f} hashes per second in pure Python)")
            break
            
        nonce += 1

if __name__ == "__main__":
    run_avalanche_demo()
    time.sleep(1)
    run_proof_of_work_demo()
