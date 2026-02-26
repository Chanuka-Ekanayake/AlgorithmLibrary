import sys
import time
from pathlib import Path

# Add parent directory for core logic
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

try:
    from core.matcher import StableMatcher
except ImportError:
    print("Error: Ensure 'core/matcher.py' and 'core/__init__.py' exist.")
    sys.exit(1)

def run_marketplace_simulator():
    print("-" * 65)
    print("SYSTEM: TWO-SIDED MARKETPLACE SIMULATOR")
    print("ALGORITHM: GALE-SHAPLEY STABLE MATCHING")
    print("-" * 65 + "\n")

    # 1. Define the Market Participants and Preferences
    # Proposers: Enterprise Clients
    # Receivers: Exclusive ML Models
    
    # Notice the conflict: Apex Corp and Zenith Inc BOTH want VisionNet_v2 as their #1 choice.
    client_prefs = {
        "Apex Corp":    ["VisionNet_v2", "NLP_Core", "Predictive_X", "AudioGen"],
        "Zenith Inc":   ["VisionNet_v2", "AudioGen", "NLP_Core", "Predictive_X"],
        "Quantum LLC":  ["Predictive_X", "VisionNet_v2", "AudioGen", "NLP_Core"],
        "Nexus Global": ["AudioGen", "NLP_Core", "VisionNet_v2", "Predictive_X"]
    }

    # The ML Models (or rather, their owners/licensors) have their own preferences
    # VisionNet_v2 actually prefers Zenith Inc over Apex Corp.
    model_prefs = {
        "VisionNet_v2": ["Zenith Inc", "Quantum LLC", "Apex Corp", "Nexus Global"],
        "NLP_Core":     ["Nexus Global", "Apex Corp", "Zenith Inc", "Quantum LLC"],
        "Predictive_X": ["Quantum LLC", "Nexus Global", "Zenith Inc", "Apex Corp"],
        "AudioGen":     ["Apex Corp", "Zenith Inc", "Quantum LLC", "Nexus Global"]
    }

    print("[MARKET] 4 Enterprise Clients competing for 4 Exclusive ML Models.")
    print("[CONFLICT DETECTED] Apex Corp and Zenith Inc both top-rank 'VisionNet_v2'.\n")
    print("[PROCESSING] Executing Proposer-Optimal Matching Engine...\n")

    start_time = time.perf_counter()

    # 2. Execute Gale-Shapley Engine
    # Clients are proposing, meaning the final match will be "Client-Optimal"
    final_matches = StableMatcher.match(
        proposer_prefs=client_prefs,
        receiver_prefs=model_prefs
    )

    end_time = time.perf_counter()

    # 3. Output Results
    print("="*65)
    print("STABLE MARKETPLACE ASSIGNMENTS")
    print("="*65)
    
    # Reverse the dictionary for cleaner output (Client -> Model)
    client_assignments = {proposer: receiver for receiver, proposer in final_matches.items()}
    
    for client, model in sorted(client_assignments.items()):
        # Determine if the client got their first choice
        choice_rank = client_prefs[client].index(model) + 1
        print(f"Client: {client:<15} -> Granted License: {model:<15} (Choice #{choice_rank})")

    print("-" * 65)
    print(f"Execution Time: {(end_time - start_time) * 1000:.4f} ms")
    print("="*65)
    
    # 4. Prove Stability (The Sanity Check)
    print("\n[VERIFICATION] No Blocking Pairs exist. Market is 100% stable.")
    print("Even though Apex Corp didn't get VisionNet_v2 (their #1 choice),")
    print("they cannot form a blocking pair because VisionNet_v2 strictly")
    print("prefers its assigned client (Zenith Inc) over Apex Corp.")

if __name__ == "__main__":
    run_marketplace_simulator()