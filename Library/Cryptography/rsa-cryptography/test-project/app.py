import sys
import os

# Add the parent directory to the path so we can import the core module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import generate_keypair, encrypt, decrypt

def main():
    print("=========================================")
    print("        RSA Cryptography Tester          ")
    print("=========================================\n")
    
    print("Generating RSA key pair (1024-bit)... This might take a moment.")
    # Generating a 1024-bit keypair
    # Note: For real-world security, 2048-bit or higher is recommended
    public_key, private_key = generate_keypair(1024)
    
    print("\n[+] Key pair generated successfully!")
    print(f"Public Key (e, n):\n  e = {public_key[0]}\n  n = ...{str(public_key[1])[-20:]} (truncated)")
    print(f"Private Key (d, n):\n  d = ...{str(private_key[0])[-20:]} (truncated)\n  n = ...{str(private_key[1])[-20:]} (truncated)")
    
    # Message to be encrypted
    message = input("\nEnter a message to encrypt: ")
    if not message:
        message = "Hello, RSA World! This is a secret message."
        print(f"Using default message: '{message}'")
    
    print(f"\nOriginal Message: {message}")
    
    # Encrypt the message
    print("\nEncrypting message with public key...")
    encrypted_msg = encrypt(public_key, message)
    
    # The encrypted message is a list of integers, let's just print a shortened version
    encrypted_str = "".join([str(c) for c in encrypted_msg])
    print(f"Encrypted Message (numerical representation):\n{encrypted_str[:50]}... (truncated)")
    
    # Decrypt the message
    print("\nDecrypting message with private key...")
    decrypted_msg = decrypt(private_key, encrypted_msg)
    
    print(f"\nDecrypted Message: {decrypted_msg}")
    
    if message == decrypted_msg:
        print("\n[SUCCESS] The decrypted message matches the original message!")
    else:
        print("\n[ERROR] The decrypted message does NOT match the original message!")

if __name__ == '__main__':
    main()
