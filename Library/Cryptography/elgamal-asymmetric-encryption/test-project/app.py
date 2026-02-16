import sys
from pathlib import Path

# Add parent directory for core logic
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

try:
    from core.elgamal import ElGamal
except ImportError:
    print("Error: Ensure 'core/elgamal.py' and 'core/__init__.py' exist.")
    sys.exit(1)

def run_licensing_sim():
    print("-" * 60)
    print("SYSTEM: SECURE LICENSING SIMULATOR")
    print("ALGORITHM: ELGAMAL ASYMMETRIC ENCRYPTION")
    print("-" * 60 + "\n")

    # 1. Initialization
    # We use a 16-bit prime for simulation speed. 
    # In production, this would be 2048+ bits.
    SAFE_PRIME = 65521 
    GENERATOR = 13
    crypto = ElGamal(p=SAFE_PRIME, g=GENERATOR)

    # 2. Key Generation (Performed by the User)
    print("[USER] Generating Public/Private key pair...")
    keys = crypto.generate_keys()
    public_key = keys["public"]
    private_key = keys["private"]
    print(f"-> Public Key (Shared with Marketplace): {public_key}")
    print(f"-> Private Key (Kept on User Machine): {private_key}\n")

    # 3. Encryption (Performed by the Marketplace Server)
    # The message is a numerical representation of a software license ID
    license_id = 42069 
    print(f"[MARKETPLACE] Preparing license ID: {license_id}")
    print("[MARKETPLACE] Encrypting with User's Public Key...")
    
    ciphertext = crypto.encrypt(license_id, public_key)
    print(f"-> Ciphertext Pair (a, b): {ciphertext}\n")

    # 4. Decryption (Performed by the User's Software Client)
    print("[CLIENT] Received encrypted license.")
    print("[CLIENT] Decrypting using Local Private Key...")
    
    decrypted_license = crypto.decrypt(ciphertext, private_key)

    # 5. Validation
    print("\n" + "="*60)
    print("LICENSE VERIFICATION REPORT")
    print("="*60)
    print(f"Original ID:       {license_id}")
    print(f"Decrypted ID:      {decrypted_license}")
    
    if license_id == decrypted_license:
        print("STATUS: SUCCESS - License Validated and Hardware Unlocked.")
    else:
        print("STATUS: FAILURE - Decryption Mismatch.")
    print("="*60)

if __name__ == "__main__":
    run_licensing_sim()