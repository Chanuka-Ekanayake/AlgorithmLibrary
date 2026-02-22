import sys
import time
import random
from pathlib import Path

# Add parent directory for core logic
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

try:
    from core.paxos import Acceptor, Proposer
except ImportError:
    print("Error: Ensure 'core/paxos.py' and 'core/__init__.py' exist.")
    sys.exit(1)

def run_paxos_simulator():
    print("-" * 65)
    print("SYSTEM: DISTRIBUTED DATABASE CONSENSUS")
    print("ALGORITHM: SINGLE-DECREE PAXOS")
    print("-" * 65 + "\n")

    # 1. Initialize the Cluster (5 Nodes)
    # A 5-node cluster requires a quorum of 3 to achieve consensus.
    # It can survive 2 simultaneous node failures.
    acceptors = [Acceptor(node_id=i) for i in range(1, 6)]
    print(f"[CLUSTER] Initialized 5 Acceptor Nodes. Quorum required: 3\n")

    # 2. Initialize Competing Proposers
    # Proposer 100 is acting for Client A
    # Proposer 200 is acting for Client B
    proposer_a = Proposer(proposer_id=100, acceptors=acceptors)
    proposer_b = Proposer(proposer_id=200, acceptors=acceptors)

    value_a = "LICENSE_SOLD_TO_CLIENT_A"
    value_b = "LICENSE_SOLD_TO_CLIENT_B"
    
    # 3. Network Chaos Configuration
    # 20% chance any given message (Prepare or Accept) is dropped by the network
    NETWORK_DROP_RATE = 0.20
    
    print(f"[NETWORK] Chaos Monkey Active: {NETWORK_DROP_RATE*100}% Packet Drop Rate")
    print(f"[TRAFFIC] Proposer A attempting to write: '{value_a}'")
    print(f"[TRAFFIC] Proposer B attempting to write: '{value_b}'\n")

    start_time = time.perf_counter()

    # 4. Simulate Concurrent Execution with Retries
    # In a real system, Proposers retry until consensus is achieved.
    consensus_reached = False
    winning_value = None
    attempts = 0

    while not consensus_reached and attempts < 10:
        attempts += 1
        print(f"--- Attempt {attempts} ---")
        
        # Proposer A tries
        success_a, final_val_a = proposer_a.run_consensus(value_a, NETWORK_DROP_RATE)
        if success_a:
            consensus_reached = True
            winning_value = final_val_a
            print(f"[SUCCESS] Proposer A achieved consensus!")
            break

        # Proposer B tries
        success_b, final_val_b = proposer_b.run_consensus(value_b, NETWORK_DROP_RATE)
        if success_b:
            consensus_reached = True
            winning_value = final_val_b
            print(f"[SUCCESS] Proposer B achieved consensus!")
            break
            
        print("[FAIL] Both Proposers failed to reach quorum (Network Drops / ID Collisions). Retrying...")
        time.sleep(0.1)

    end_time = time.perf_counter()

    # 5. Final State Verification
    print("\n" + "="*65)
    print("CLUSTER STATE REPORT")
    print("="*65)
    print(f"Global Consensus Value: {winning_value}")
    print("-" * 65)
    
    # Verify the internal state of every node to prove no split-brain occurred
    for acc in acceptors:
        state = acc.accepted_value if acc.accepted_value else "NULL"
        print(f"Node {acc.node_id} Final Written State: {state}")

    print("-" * 65)
    print(f"Time to Consensus: {(end_time - start_time) * 1000:.4f} ms")
    print("="*65)

    # Mathematical safety check: Ensure no two nodes accepted DIFFERENT non-null values
    accepted_states = set(acc.accepted_value for acc in acceptors if acc.accepted_value is not None)
    assert len(accepted_states) <= 1, "CRITICAL ERROR: SPLIT BRAIN DETECTED!"
    
    if len(accepted_states) == 1:
        print("RESULT: 100% Data Consistency Maintained. No Split-Brain.")
    else:
        print("RESULT: Consensus failed completely. Data was protected from corruption.")

if __name__ == "__main__":
    run_paxos_simulator()