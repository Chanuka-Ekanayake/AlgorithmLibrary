import sys
import time
from pathlib import Path

# Add parent directory for core logic
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

try:
    from core.arithmetic import ArithmeticCoder
except ImportError:
    print("Error: Ensure 'core/arithmetic.py' and 'core/__init__.py' exist.")
    sys.exit(1)

def run_dna_compressor():
    print("-" * 65)
    print("SYSTEM: DNA SEQUENCE COMPRESSOR")
    print("ALGORITHM: ARITHMETIC CODING (FRACTIONAL ENTROPY)")
    print("-" * 65 + "\n")

    # 1. Simulated genetic sequence (Repetitive to show entropy benefits)
    dna_sequence = "GATTACAGATTACAGATTACA"
    seq_length = len(dna_sequence)

    print(f"[DATA] Original Sequence: {dna_sequence}")
    print(f"[DATA] Sequence Length:   {seq_length} characters\n")

    # 2. Initialize the Arithmetic Coder
    # We use high precision to ensure we don't lose data on longer strings
    print("[PROCESSING] Generating Cumulative Probability Table...")
    coder = ArithmeticCoder(text=dna_sequence, precision=150)
    
    for char, (low, high) in coder.probability_table.items():
        print(f"       -> '{char}' Interval: [{low:.4f}, {high:.4f})")
    print()

    # 3. Encode the sequence
    print("[ENCODING] Compressing sequence into a single fraction...")
    start_encode = time.perf_counter()
    encoded_fraction = coder.encode(dna_sequence)
    end_encode = time.perf_counter()

    # Print a truncated version of the massive decimal
    truncated_fraction = str(encoded_fraction)[:40] + "..."
    print(f"       -> Encoded Value: {truncated_fraction}\n")

    # 4. Decode the sequence
    print("[DECODING] Reconstructing sequence from fractional value...")
    start_decode = time.perf_counter()
    decoded_sequence = coder.decode(encoded_fraction, seq_length)
    end_decode = time.perf_counter()

    # 5. Validation
    if dna_sequence != decoded_sequence:
        raise RuntimeError("CRITICAL ERROR: Data loss detected.")

    print("\n" + "="*65)
    print("COMPRESSION REPORT")
    print("="*65)
    print(f"Original Text: {dna_sequence}")
    print(f"Decoded Text:  {decoded_sequence}")
    print("-" * 65)
    print("PERFORMANCE METRICS:")
    print(f"Encoding Time: {(end_encode - start_encode) * 1000:.4f} ms")
    print(f"Decoding Time: {(end_decode - start_decode) * 1000:.4f} ms")
    print("="*65)
    print("RESULT: 100% Lossless reconstruction achieved.")

if __name__ == "__main__":
    run_dna_compressor()