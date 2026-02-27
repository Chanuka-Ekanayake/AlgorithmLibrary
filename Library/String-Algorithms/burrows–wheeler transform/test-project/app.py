import sys
import time
from pathlib import Path
from itertools import groupby

# Add parent directory for core logic
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

try:
    from core.transform import BurrowsWheeler
except ImportError:
    print("Error: Ensure 'core/transform.py' and 'core/__init__.py' exist.")
    sys.exit(1)

def count_runs(text: str) -> int:
    """Calculates the number of consecutive character blocks (runs)."""
    # groupby groups consecutive identical elements. 
    # e.g., "aaabbc" -> ['a', 'b', 'c'] (3 runs)
    return len(list(groupby(text)))

def run_bwt_simulator():
    print("-" * 65)
    print("SYSTEM: SOFTWARE BINARY PRE-COMPRESSOR")
    print("ALGORITHM: BURROWS-WHEELER TRANSFORM (BWT)")
    print("-" * 65 + "\n")

    # 1. Simulated Data
    # We use a structured payload typical of an ML model metadata array
    # Notice the repetitive keys, but they are spread out.
    raw_data = (
        '{"model":"VisionNet","type":"CNN","status":"active"},'
        '{"model":"AudioGen","type":"RNN","status":"active"},'
        '{"model":"TextNet","type":"RNN","status":"active"},'
        '{"model":"PredictiveX","type":"CNN","status":"active"}'
    )
    
    print("[INPUT] Original ML Model Metadata Array:")
    print(f"'{raw_data}'\n")

    original_runs = count_runs(raw_data)
    print(f"[METRIC] Original Sequence Runs: {original_runs}")
    print("         (High variance means poor compression efficiency)\n")

    # 2. Forward Transform (Pre-processing)
    print("[PROCESSING] Applying Forward Burrows-Wheeler Transform...")
    start_time = time.perf_counter()
    
    bwt_string = BurrowsWheeler.transform(raw_data)
    
    forward_time = time.perf_counter()

    print("\n[OUTPUT] BWT Transformed String:")
    # Highlighting the output to show the character groupings clearly
    print(f"'{bwt_string}'\n")

    bwt_runs = count_runs(bwt_string)
    print(f"[METRIC] Transformed Sequence Runs: {bwt_runs}")
    
    run_reduction = ((original_runs - bwt_runs) / original_runs) * 100
    print(f"[METRIC] Run Reduction: {run_reduction:.1f}%")
    print("         (Identical characters are now clustered, ready for RLE/Arithmetic Coding)\n")

    # 3. Inverse Transform (Reconstruction)
    print("[PROCESSING] Reversing transform via O(N) LF Mapping...")
    
    inverse_start = time.perf_counter()
    reconstructed_data = BurrowsWheeler.inverse(bwt_string)
    inverse_time = time.perf_counter()

    # 4. Verification
    print("\n" + "="*65)
    print("DATA INTEGRITY REPORT")
    print("="*65)
    print(f"Original Text:      {raw_data[:40]}...")
    print(f"Reconstructed Text: {reconstructed_data[:40]}...")
    print("-" * 65)
    
    if raw_data == reconstructed_data:
        print("[SUCCESS] 100% Lossless Reconstruction Achieved.")
    else:
        print("[FATAL] Data corruption detected during reconstruction.")
        
    print(f"Forward Execution Time: {(forward_time - start_time) * 1000:.4f} ms")
    print(f"Inverse Execution Time: {(inverse_time - inverse_start) * 1000:.4f} ms")
    print("="*65)

if __name__ == "__main__":
    run_bwt_simulator()