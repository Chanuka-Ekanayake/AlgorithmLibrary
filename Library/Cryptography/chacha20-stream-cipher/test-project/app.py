import sys
import os
import time
from pathlib import Path

# Resolve project root so imports work from any working directory
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

try:
    from core.chacha20 import ChaCha20
except ImportError:
    print("Error: Ensure 'core/chacha20.py' and 'core/__init__.py' exist.")
    sys.exit(1)


def separator(char: str = "-", width: int = 68) -> None:
    print(char * width)


def format_hex(data: bytes) -> str:
    """Formats bytes into a readable hex string."""
    hex_str = data.hex()
    return " ".join(hex_str[i:i+8] for i in range(0, len(hex_str), 8))


def run_secure_messaging_simulation() -> None:
    separator("=")
    print("SYSTEM: SECURE MESSAGING ENCLAVE")
    print("ALGORITHM: ChaCha20 STREAM CIPHER")
    separator("=")
    print()

    # 1. Generate Key and Nonce
    # In a real system, the key would be derived securely (e.g. PBKDF2, Argon2)
    # or established via a key exchange protocol (e.g. ECDHE).
    print("[SYSTEM] Generating 256-bit Key and 96-bit Nonce...")
    key = os.urandom(32)
    nonce = os.urandom(12)
    
    print(f"Key (256-bit)   : {format_hex(key)}")
    print(f"Nonce (96-bit)  : {format_hex(nonce)}")
    print()

    # 2. Define the message
    plaintext_msg = (
        "CONFIDENTIAL: The perimeter has been breached. "
        "Initiate protocol alpha immediately. "
        "Do not trust unverified communications over the primary channel."
    )
    plaintext_bytes = plaintext_msg.encode('utf-8')
    
    print("[TX] Original Plaintext Message:")
    print(f"     \"{plaintext_msg}\"")
    print(f"     Length: {len(plaintext_bytes)} bytes")
    print()

    # 3. Encrypt the message
    print("[PROCESSING] Encrypting message using ChaCha20...")
    
    cipher_tx = ChaCha20(key, nonce)
    
    t0 = time.perf_counter()
    ciphertext = cipher_tx.encrypt(plaintext_bytes)
    t1 = time.perf_counter()
    encrypt_ms = (t1 - t0) * 1000
    
    print(f"[OK] Encryption completed in {encrypt_ms:.4f} ms")
    print()
    
    print("[NETWORK] Ciphertext Payload (Hex):")
    print(f"          {format_hex(ciphertext)}")
    print()

    # 4. Decrypt the message
    # The receiver instances a new ChaCha20 with the same key and nonce
    print("[RX] Receiving message and decrypting...")
    
    cipher_rx = ChaCha20(key, nonce)
    
    t0 = time.perf_counter()
    decrypted_bytes = cipher_rx.decrypt(ciphertext)
    t1 = time.perf_counter()
    decrypt_ms = (t1 - t0) * 1000
    
    decrypted_msg = decrypted_bytes.decode('utf-8')
    
    print(f"[OK] Decryption completed in {decrypt_ms:.4f} ms")
    print()
    
    print("[RX] Decrypted Plaintext Message:")
    print(f"     \"{decrypted_msg}\"")
    print()

    # 5. Verification
    separator()
    if plaintext_msg == decrypted_msg:
        print("[SUCCESS] Integrity Confirmed: Decrypted text matches original plaintext.")
    else:
        print("[ERROR] Integrity Failure: Decrypted text DOES NOT match original plaintext.")
    separator("=")


if __name__ == "__main__":
    run_secure_messaging_simulation()
