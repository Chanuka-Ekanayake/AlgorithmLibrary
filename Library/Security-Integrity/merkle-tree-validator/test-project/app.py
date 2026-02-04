import sys
from pathlib import Path

# Add parent directory to path for core logic access
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

try:
    from core.merkle_tree import MerkleTree
except ImportError:
    print("Error: Ensure 'core/merkle_tree.py' and 'core/__init__.py' exist.")
    sys.exit(1)

def run_integrity_simulation():
    print("--------------------------------------------------")
    print("SYSTEM: BINARY PAYLOAD INTEGRITY SHIELD")
    print("ALGORITHM: MERKLE TREE (SHA-256)")
    print("--------------------------------------------------\n")

    # 1. Simulate a large ML Model broken into 8 chunks
    ml_model_chunks = [
        "weights_layer_1_001", "weights_layer_1_002",
        "weights_layer_2_001", "weights_layer_2_002",
        "bias_vectors_001",    "bias_vectors_002",
        "metadata_v1.0",       "optimizer_state"
    ]
    
    print(f"[SERVER] Generating Merkle Tree for {len(ml_model_chunks)} data blocks...")
    tree = MerkleTree(ml_model_chunks)
    root_hash = tree.get_root_hash()
    print(f"[SERVER] Trusted Merkle Root: {root_hash}\n")

    # 2. Client Side: Verifying a legitimate block (Chunk 3)
    target_index = 2
    target_data = ml_model_chunks[target_index]
    print(f"[CLIENT] Verifying Block #{target_index} ('{target_data}')...")
    
    proof = tree.get_proof(target_index)
    is_valid = MerkleTree.verify_proof(target_data, proof, root_hash)
    
    if is_valid:
        print("VERIFICATION SUCCESS: Data block is authentic.")
    else:
        print("VERIFICATION FAILED: Data block is corrupted.")

    # 3. Simulation: Data Tampering (Man-in-the-Middle)
    print("\n[ATTACK] Man-in-the-middle tampering with Block #6...")
    tampered_data = "bias_vectors_002_MALICIOUS_CODE"
    tampered_index = 5
    
    # Client tries to verify the tampered block using the original proof and root
    print(f"[CLIENT] Verifying Block #{tampered_index}...")
    tamper_proof = tree.get_proof(tampered_index)
    is_tamper_valid = MerkleTree.verify_proof(tampered_data, tamper_proof, root_hash)

    if not is_tamper_valid:
        print("ALERT: TAMPERING DETECTED! The block hash does not match the Merkle Root.")
    else:
        print("Warning: Tampering went undetected (Logic error).")

    print("\n--------------------------------------------------")
    print("STATUS: INTEGRITY VERIFIED")
    print("Merkle Tree successfully protected the payload.")
    print("--------------------------------------------------")

if __name__ == "__main__":
    run_integrity_simulation()