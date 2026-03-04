import sys
import time
from pathlib import Path

# Add parent directory for core logic
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

try:
    from core.cipher import BlowfishCipher
except ImportError:
    print("Error: Ensure 'core/cipher.py' and 'core/__init__.py' exist.")
    sys.exit(1)

def pad_data(data: bytes, block_size: int = 8) -> bytes:
    """Applies PKCS5 padding to ensure data is a multiple of the block size."""
    padding_len = block_size - (len(data) % block_size)
    # Append the byte value of the padding length, padding_len times
    return data + bytes([padding_len] * padding_len)

def unpad_data(data: bytes) -> bytes:
    """Removes PKCS5 padding after decryption."""
    padding_len = data[-1]
    return data[:-padding_len]

def run_encryptor_simulator():
    print("-" * 65)
    print("SYSTEM: SOFTWARE LICENSE KEY ENCRYPTOR")
    print("ENGINE: BLOWFISH SYMMETRIC CIPHER (ECB MODE)")
    print("-" * 65 + "\n")

    # 1. Initialize the Master Key and Payload
    # The secret key stored securely on your backend server
    master_secret = b"E-COMMERCE-MASTER-KEY-2026" 
    
    # The plaintext payload to be securely transmitted to the buyer
    license_payload = b"ML-MODEL-PRO-VALID-USER-9984"

    print(f"[STORE] Master Secret Key:  {master_secret.decode('utf-8')}")
    print(f"[ORDER] Plaintext Payload:  {license_payload.decode('utf-8')}\n")

    # 2. Key Expansion (The Slow Setup)
    print("[PROCESSING] Initializing Cipher State (Key Expansion)...")
    start_setup = time.perf_counter()
    cipher = BlowfishCipher(master_secret)
    end_setup = time.perf_counter()
    print(f"         521 Setup Encryptions finished in {(end_setup - start_setup) * 1000:.2f} ms.\n")

    # 3. Data Formatting (Padding)
    padded_payload = pad_data(license_payload)
    print(f"[FORMAT] Padded Data (Hex): {padded_payload.hex().upper()}")

    # 4. Encryption Phase (The Fast Execution)
    print("\n[PROCESSING] Encrypting Payload...")
    start_enc = time.perf_counter()
    
    ciphertext = bytearray()
    # Process the data in strict 8-byte blocks
    for i in range(0, len(padded_payload), 8):
        block = padded_payload[i:i+8]
        encrypted_block = cipher.encrypt_block(block)
        ciphertext.extend(encrypted_block)
        
    end_enc = time.perf_counter()
    
    print("\n" + "=" * 65)
    print("TRANSMISSION READY (CIPHERTEXT)")
    print("=" * 65)
    print(f"Encrypted Hex: {ciphertext.hex().upper()}")
    print("=" * 65 + "\n")

    # 5. Decryption Phase (Simulating the Buyer's Machine)
    print("[PROCESSING] Decrypting Payload on Client Side...")
    start_dec = time.perf_counter()
    
    decrypted_padded = bytearray()
    for i in range(0, len(ciphertext), 8):
        block = ciphertext[i:i+8]
        decrypted_block = cipher.decrypt_block(block)
        decrypted_padded.extend(decrypted_block)
        
    # Strip the padding to reveal the original string
    final_plaintext = unpad_data(decrypted_padded)
    end_dec = time.perf_counter()

    print("\n" + "=" * 65)
    print("DECRYPTION RESULT")
    print("=" * 65)
    print(f"Recovered Payload: {final_plaintext.decode('utf-8')}")
    print("-" * 65)
    print(f"Encryption Time:   {(end_enc - start_enc) * 1000:.4f} ms")
    print(f"Decryption Time:   {(end_dec - start_dec) * 1000:.4f} ms")
    print("=" * 65)

if __name__ == "__main__":
    run_encryptor_simulator()