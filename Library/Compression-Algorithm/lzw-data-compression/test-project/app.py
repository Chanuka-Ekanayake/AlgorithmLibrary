import sys
import os

# Add the parent directory to the path so we can import the core module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.lzw import LZWCompressor

def main():
    print("--- LZW Data Compressor ---")
    
    # Read sample data
    sample_file = os.path.join(os.path.dirname(__file__), "sample_data.txt")
    
    try:
        with open(sample_file, "r", encoding="utf-8") as f:
            data = f.read()
    except FileNotFoundError:
        print(f"Error: Could not find {sample_file}")
        return

    print(f"\n[1] Original Data Length: {len(data)} characters")
    print(f"Original Data Preview: {data[:50]}...")

    # Initialize compressor
    compressor = LZWCompressor()

    # Compress
    print("\n[2] Compressing data...")
    compressed_data, ratio = compressor.compress(data)
    
    print(f"Compressed Data Length: {len(compressed_data)} codes")
    print(f"Compression Ratio Estimate: {ratio} (lower is better)")
    print(f"Compressed Data Preview: {compressed_data[:10]}...")

    # Decompress
    print("\n[3] Decompressing data...")
    decompressed_data = compressor.decompress(compressed_data)
    print(f"Decompressed Data Length: {len(decompressed_data)} characters")
    
    # Verify
    print("\n[4] Verification...")
    if data == decompressed_data:
        print("SUCCESS: Decompressed data exactly matches the original!")
    else:
        print("ERROR: Decompressed data does not match the original.")

if __name__ == "__main__":
    main()
