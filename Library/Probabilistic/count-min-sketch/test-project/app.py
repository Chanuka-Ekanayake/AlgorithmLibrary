import sys
import random
from collections import Counter
from pathlib import Path

# Add parent directory to path for core logic access
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

try:
    from core.cms import CountMinSketch
except ImportError:
    print("❌ Error: Ensure 'core/cms.py' and 'core/__init__.py' exist.")
    sys.exit(1)

def run_trending_simulation():
    print("--------------------------------------------------")
    print("SYSTEM: TRENDING MODEL TRACKER")
    print("ALGORITHM: COUNT-MIN SKETCH (FREQUENCY ESTIMATOR)")
    print("--------------------------------------------------\n")

    # 1. Configuration
    TOTAL_DOWNLOADS = 100000
    UNIQUE_MODELS = 500
    # We'll use a relatively small sketch for demonstration (Width: 400, Depth: 5)
    cms = CountMinSketch(width=400, depth=5)
    exact_counter = Counter()

    print(f"[SIMULATE] Generating {TOTAL_DOWNLOADS:,} download events...")
    
    # Generate model IDs (Model_0 to Model_499)
    # We use a weighted distribution so some models are "Viral"
    models = [f"Model_{i}" for i in range(UNIQUE_MODELS)]
    # Weights: Model_0 is very popular, Model_499 is rare
    weights = [1.0 / (i + 1) for i in range(UNIQUE_MODELS)]

    # Precompute cumulative weights once to avoid recomputing them in the loop
    cum_weights = []
    total_weight = 0.0
    for w in weights:
        total_weight += w
        cum_weights.append(total_weight)

    for _ in range(TOTAL_DOWNLOADS):
        # Pick a model based on the popularity weights (Zipf-like distribution)
        model_id = random.choices(models, cum_weights=cum_weights, k=1)[0]
        
        # Update both exact and probabilistic structures
        exact_counter[model_id] += 1
        cms.add(model_id)

    # 2. Results Comparison
    print("\n" + "="*60)
    print(f"{'MODEL ID':<15} | {'EXACT COUNT':<15} | {'CMS ESTIMATE':<15} | {'ERROR'}")
    print("="*60)

    # Check the top 10 most popular models
    top_models = [m for m, _ in exact_counter.most_common(10)]
    # Add a few rare models to see how it handles the "Long Tail"
    rare_models = [f"Model_{UNIQUE_MODELS - 1}", f"Model_{UNIQUE_MODELS - 50}"]
    
    for model_id in top_models + rare_models:
        actual = exact_counter[model_id]
        estimate = cms.estimate(model_id)
        error = estimate - actual
        print(f"{model_id:<15} | {actual:<15,} | {estimate:<15,} | +{error}")

    # 3. Memory Audit
    # Python dict entries are approx 24-48 bytes each + key/value strings
    exact_memory_kb = (len(exact_counter) * 128) / 1024 
    # Theoretical CMS size assuming packed 32-bit (4-byte) counters: width * depth * 4 bytes
    cms_memory_kb = (cms.width * cms.depth * 4) / 1024

    print("\n" + "-"*60)
    print(f"RESOURCES USED")
    print("-" * 60)
    print(f"Standard Dictionary Memory (approx.):              ~{exact_memory_kb:.2f} KB")
    print(f"Count-Min Sketch Memory (theoretical 32-bit):      ~{cms_memory_kb:.2f} KB")
    print(f"Accuracy for Heavy Hitters: High (Conservative Estimate)")
    print("="*60)

if __name__ == "__main__":
    run_trending_simulation()