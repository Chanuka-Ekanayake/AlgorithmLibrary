import threading
import time
import sys
from pathlib import Path

# Add parent directory to path for core logic access
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

try:
    from core.raft_node import RaftNode, State
except ImportError:
    print("Error: Ensure 'core/raft_node.py' and 'core/__init__.py' exist.")
    sys.exit(1)

class ClusterSimulator:
    def __init__(self, node_count=5):
        self.nodes = {}
        node_ids = list(range(node_count))
        for i in node_ids:
            peers = [p for p in node_ids if p != i]
            self.nodes[i] = RaftNode(i, peers)
        self.running = True

    def run_node(self, node_id):
        """Simulates the lifecycle of a single Raft node."""
        node = self.nodes[node_id]
        while self.running:
            # 1. Execute node logic (check timeouts, send heartbeats)
            node.tick()

            # 2. If node is a Candidate, simulate sending RPCs to peers
            if node.state == State.CANDIDATE:
                for peer_id in node.peer_ids:
                    # Simulate network call: RequestVote
                    granted = self.nodes[peer_id].handle_request_vote(node.current_term, node.node_id)
                    node.handle_vote_response(node.current_term, granted, peer_id)

            # 3. If node is a Leader, simulate sending heartbeats
            if node.state == State.LEADER:
                for peer_id in node.peer_ids:
                    self.nodes[peer_id].handle_heartbeat(node.current_term, node.node_id)

            time.sleep(0.05) # Loop frequency

    def get_leader(self):
        for node_id, node in self.nodes.items():
            if node.state == State.LEADER:
                return node_id
        return None

def start_simulation():
    print("--------------------------------------------------")
    print("SYSTEM: CLUSTER CHAOS SIMULATOR")
    print("ALGORITHM: RAFT CONSENSUS (LEADER ELECTION)")
    print("--------------------------------------------------\n")

    sim = ClusterSimulator(node_count=5)
    threads = []

    # Start all nodes in separate threads
    for node_id in sim.nodes.keys():
        t = threading.Thread(target=sim.run_node, args=(node_id,), daemon=True)
        t.start()
        threads.append(t)

    print("[SYSTEM] Cluster started. Waiting for initial election...")
    time.sleep(2)

    initial_leader = sim.get_leader()
    print(f"\n🏆 [STABILITY] Current Cluster Leader: Node {initial_leader}")
    print("--------------------------------------------------")
    
    # SIMULATE CHAOS: Kill the Leader
    print(f"🔥 [CHAOS] Simulating CRASH of Leader (Node {initial_leader})...")
    # We 'stop' the node logic for this ID
    sim.nodes[initial_leader].state = State.FOLLOWER # Strip authority
    # Move it to a term in the past so it can't interfere
    sim.nodes[initial_leader].current_term = -1 
    # Stop its heartbeats by technically 'pausing' it (it won't tick in our sim loop)
    # For simulation purposes, we just watch the others react to the lack of heartbeats.
    
    print("[SYSTEM] Monitoring cluster for re-election...")
    time.sleep(2)

    new_leader = sim.get_leader()
    if new_leader is not None and new_leader != initial_leader:
        print(f"\n✨ [HEALED] New Leader Elected: Node {new_leader}")
        print(f"[INFO] Node {new_leader} successfully achieved Quorum.")
    else:
        print("\n⚠️ [PENDING] Cluster is still in transition or split-vote state.")

    sim.running = False
    print("\n--------------------------------------------------")
    print("STATUS: SIMULATION COMPLETE")
    print("--------------------------------------------------")

if __name__ == "__main__":
    start_simulation()