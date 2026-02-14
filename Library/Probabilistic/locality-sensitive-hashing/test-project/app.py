import sys
import time
from pathlib import Path

# --- ENVIRONMENT CHECK ---
try:
    import numpy as np
except ImportError:
    print("ERROR: NumPy not found.")
    print("Please run: pip install numpy")
    sys.exit(1)

# Add parent directory to path for core logic access
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

try:
    from core.lsh import RandomProjectionLSH
except ImportError:
    print("Error: Ensure 'core/lsh.py' and 'core/__init__.py' exist.")
    sys.exit(1)

def run_similarity_sim():
    print("--------------------------------------------------")
    print("SYSTEM: SIMILAR MODEL FINDER")
    print("ALGORITHM: LOCALITY-SENSITIVE HASHING (LSH)")
    print("--------------------------------------------------\n")

    # 1. Configuration
    DIMENSIONS = 128      # Size of the model embedding
    NUM_MODELS = 1000     # Total models in our marketplace
    PROJECTIONS = 12      # Number of 'fences' (creates 2^12 buckets)

    lsh = RandomProjectionLSH(dimensions=DIMENSIONS, num_projections=PROJECTIONS)

    # 2. Generate and Index Random Models
    print(f"[INDEXING] Creating {NUM_MODELS} model embeddings...")
    model_database = {}
    
    for i in range(NUM_MODELS):
        model_id = f"ML_Model_{i:03d}"
        # Generate a random vector for each model
        vector = np.random.randn(DIMENSIONS).tolist()
        model_database[model_id] = vector
        lsh.add_item(model_id, vector)

    # 3. Create a 'Query Model' 
    # We'll take an existing model and add a tiny bit of noise to simulate a 'similar' one
    target_id = "ML_Model_42"
    target_vector = np.array(model_database[target_id])
    query_vector = (target_vector + np.random.normal(0, 0.1, DIMENSIONS)).tolist()

    print(f"[QUERY] Searching for models similar to '{target_id}'...")
    
    # 4. Perform LSH Query
    start_time = time.time()
    candidates = lsh.query(query_vector)
    end_time = time.time()

    # 5. Results
    print("\n" + "="*50)
    print("SIMILARITY SEARCH REPORT")
    print("="*50)
    print(f"Search Time:        {(end_time - start_time)*1000:.4f} ms")
    print(f"Total Database:     {NUM_MODELS} models")
    print(f"Candidates Found:   {len(candidates)}")
    print(f"Bucket Density:     {len(candidates)/NUM_MODELS*100:.2f}% of database scanned")
    print("-" * 50)
    
    if target_id in candidates:
        print(f"RESULT: Found '{target_id}' in the same bucket!")
    else:
        print(f"RESULT: '{target_id}' was not found (Probabilistic Miss).")
        print("Tip: Use more hash tables (OR-amplification) to increase recall.")
    
    print("\n[STATS]:", lsh.get_stats())
    print("="*50)

if __name__ == "__main__":
    run_similarity_sim()