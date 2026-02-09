import sys
import time
import random
from pathlib import Path

# Add parent directory to path for core logic access
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

try:
    from core.gossip_node import GossipNode
except ImportError:
    print("Error: Ensure 'core/gossip_node.py' and 'core/__init__.py' exist.")
    sys.exit(1)

def run_rumor_simulation():
    print("--------------------------------------------------")
    print("SYSTEM: THE RUMOR MILL")
    print("ALGORITHM: GOSSIP PROTOCOL (EPIDEMIC BROADCAST)")
    print("--------------------------------------------------\n")

    NODE_COUNT = 20
    nodes = []

    # 1. Initialize the cluster
    # Every node knows every other node's ID in this simple mesh
    all_ids = list(range(NODE_COUNT))
    for i in all_ids:
        peers = [p for p in all_ids if p != i]
        nodes.append(GossipNode(i, peers))

    # 2. Inject the "Secret Rumor" into Node 0
    SECRET_KEY = "marketplace_alert"
    SECRET_VAL = "Critical Update: Version 2.0 Released"
    print(f"[INJECT] Dropping secret into Node 0...")
    nodes[0].inject_data(SECRET_KEY, SECRET_VAL)

    # 3. Simulation Loop
    round_num = 0
    fully_informed = False

    while not fully_informed:
        round_num += 1
        # Track who knows the secret this round
        informed_nodes = [n.node_id for n in nodes if n.get_value(SECRET_KEY)]
        
        # Visualization
        progress = ["█" if i in informed_nodes else "░" for i in range(NODE_COUNT)]
        print(f"Round {round_num:02d}: [{' '.join(progress)}] ({len(informed_nodes)}/{NODE_COUNT} nodes)")

        if len(informed_nodes) == NODE_COUNT:
            fully_informed = True
            break

        # Each node gossips with random peers
        # We simulate the network calls by passing knowledge maps
        for node in nodes:
            targets = node.select_gossip_targets()
            payload = node.prepare_gossip_payload()
            for target_id in targets:
                nodes[target_id].receive_gossip(payload)
        
        time.sleep(0.4) # Pause for visual effect

    print("\n" + "="*50)
    print("FINAL CONVERGENCE REPORT")
    print("="*50)
    print(f"Total Cluster Size:     {NODE_COUNT} Nodes")
    print(f"Rounds to Converge:     {round_num}")
    print(f"Consistency Status:     EVENTUALLY CONSISTENT")
    print("-" * 50)
    print(f"Final Data at Node {random.randint(0, NODE_COUNT-1)}: {nodes[0].get_value(SECRET_KEY)}")
    print("="*50)

if __name__ == "__main__":
    run_rumor_simulation()