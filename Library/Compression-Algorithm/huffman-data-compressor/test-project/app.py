import sys
import os

# Add parent directory to path for core logic access
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.huffman import HuffmanCoder

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_sample_data(filepath):
    """Reads the raw text from the sample file."""
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return ""

def run_compression_simulation():
    clear_screen()
    print("--------------------------------------------------")
    print("SYSTEM: BINARY PAYLOAD OPTIMIZER")
    print("ALGORITHM: HUFFMAN LOSSLESS COMPRESSION")
    print("--------------------------------------------------\n")

    # 1. Load Data
    raw_text = load_sample_data('sample_data.txt')
    if not raw_text:
        return

    # 2. Initialize and Compress
    coder = HuffmanCoder()
    bitstring, ratio = coder.compress(raw_text)

    # 3. Output Professional Report
    print(f"ANALYSIS COMPLETE:")
    print(f"  Original Size:   {len(raw_text) * 8} bits")
    print(f"  Compressed Size: {len(bitstring)} bits")
    print(f"  Space Saved:     {ratio * 100:.2f}%")
    print("--------------------------------------------------\n")

    print("GENERATED HUFFMAN DICTIONARY (Partial):")
    # Show first 5 codes for brevity
    display_count = 0
    for char, code in sorted(coder.encoder.items(), key=lambda x: len(x[1])):
        char_display = char.replace('\n', '\\n').replace(' ', '[Space]')
        print(f"  '{char_display}': {code}")
        display_count += 1
        if display_count >= 8: break
    print("  ...")

    print("\n--------------------------------------------------")
    print("VERIFICATION: Decompressing payload...")
    decompressed = coder.decompress(bitstring)
    
    if decompressed == raw_text:
        print("STATUS: SUCCESS (100% Data Integrity Verified)")
    else:
        print("STATUS: ERROR (Data Mismatch Detected)")
    print("--------------------------------------------------")

if __name__ == "__main__":
    run_compression_simulation()