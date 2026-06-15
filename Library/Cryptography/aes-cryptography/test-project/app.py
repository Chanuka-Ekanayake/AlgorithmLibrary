import sys
import os
import time
from pathlib import Path

# Resolve project root so imports work from any working directory
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

try:
    from core.aes import AES
except ImportError:
    print("Error: Ensure 'core/aes.py' and 'core/__init__.py' exist.")
    sys.exit(1)


def separator(char: str = "-", width: int = 72) -> None:
    print(char * width)


def format_hex(data: bytes) -> str:
    """Formats bytes into space-separated 8-character hex blocks."""
    hex_str = data.hex()
    return " ".join(hex_str[i:i+8] for i in range(0, len(hex_str), 8))


def run_ecb_vs_cbc_demo() -> None:
    separator("=")
    print("DEMO: BLOCK CIPHER MODE COMPARISON (ECB VS CBC)")
    print("PLaintext contains repeating 16-byte patterns.")
    separator("=")

    # Define a 16-byte pattern repeated 4 times (64 bytes total)
    pattern = b"ATTACK_AT_DAWN!!"
    plaintext = pattern * 4

    print(f"Plaintext (64 bytes, 4 blocks of '{pattern.decode()}'):")
    print(f"Hex: {format_hex(plaintext)}")
    print()

    # Generate key and IV
    key = os.urandom(32)  # 256-bit key
    iv = os.urandom(16)   # 128-bit IV
    cipher = AES(key)

    # Encrypt with ECB and CBC
    ciphertext_ecb = cipher.encrypt_ecb(plaintext)
    ciphertext_cbc = cipher.encrypt_cbc(plaintext, iv)

    print("ECB MODE CIPHERTEXT:")
    for b in range(4):
        block = ciphertext_ecb[b*16 : (b+1)*16]
        print(f"  Block {b+1}: {block.hex()}")
    print("-> Notice how Block 1, 2, 3, and 4 are EXACTLY identical because ECB encrypts each block independently.")
    print()

    print("CBC MODE CIPHERTEXT:")
    for b in range(4):
        block = ciphertext_cbc[b*16 : (b+1)*16]
        print(f"  Block {b+1}: {block.hex()}")
    print("-> Notice how all blocks are completely different, because each block is chained with the previous ciphertext block.")
    print()


def run_benchmarking() -> None:
    separator("=")
    print("BENCHMARK: AES KEY SIZES & SPEEDS")
    separator("=")

    payload = b"Performance testing payload. " * 500  # ~14.5 KB
    print(f"Payload size: {len(payload)} bytes")
    print(f"{"Key Size":<12} | {"Key Expansion":<16} | {"Encryption":<12} | {"Decryption":<12}")
    separator("-")

    for bit_size in [128, 192, 256]:
        byte_size = bit_size // 8
        key = os.urandom(byte_size)
        iv = os.urandom(16)

        # Benchmark Key Expansion
        t0 = time.perf_counter()
        cipher = AES(key)
        t_expansion = (time.perf_counter() - t0) * 1000  # ms

        # Benchmark Encryption (CBC)
        t0 = time.perf_counter()
        ciphertext = cipher.encrypt_cbc(payload, iv)
        t_encrypt = (time.perf_counter() - t0) * 1000  # ms

        # Benchmark Decryption (CBC)
        t0 = time.perf_counter()
        decrypted = cipher.decrypt_cbc(ciphertext, iv)
        t_decrypt = (time.perf_counter() - t0) * 1000  # ms

        # Assert correctness
        assert decrypted == payload, f"Decryption failure for AES-{bit_size}"

        print(f"AES-{bit_size:<8} | {t_expansion:>13.4f} ms | {t_encrypt:>9.4f} ms | {t_decrypt:>9.4f} ms")
    print()


def run_interactive_demo() -> None:
    separator("=")
    print("INTERACTIVE DEMO: ENCRYPT CUSTOM MESSAGE")
    separator("=")

    message = input("Enter a message to encrypt (or press Enter for default): ").strip()
    if not message:
        message = "Deploy forces to sectors 4 and 7. Code red."

    plaintext = message.encode("utf-8")
    key = os.urandom(32)  # 256-bit key
    iv = os.urandom(16)

    print()
    print(f"Original text : {message}")
    print(f"Plaintext Hex : {format_hex(plaintext)}")
    print()

    cipher = AES(key)

    # CBC Mode
    ciphertext_cbc = cipher.encrypt_cbc(plaintext, iv)
    decrypted_cbc = cipher.decrypt_cbc(ciphertext_cbc, iv)

    print("[CBC Mode]")
    print(f"  Ciphertext (Hex): {format_hex(ciphertext_cbc)}")
    print(f"  Decrypted text  : {decrypted_cbc.decode('utf-8')}")
    print()

    # ECB Mode
    ciphertext_ecb = cipher.encrypt_ecb(plaintext)
    decrypted_ecb = cipher.decrypt_ecb(ciphertext_ecb)

    print("[ECB Mode]")
    print(f"  Ciphertext (Hex): {format_hex(ciphertext_ecb)}")
    print(f"  Decrypted text  : {decrypted_ecb.decode('utf-8')}")
    print()


def main() -> None:
    separator("=")
    print("SYSTEM: AES (ADVANCED ENCRYPTION STANDARD) SIMULATOR")
    separator("=")
    print()

    run_ecb_vs_cbc_demo()
    run_benchmarking()
    
    # Check if running in automated/non-interactive test environment
    if len(sys.argv) > 1 and sys.argv[1] == "--non-interactive":
        print("Non-interactive mode requested. Skipping custom message input.")
        return
        
    try:
        run_interactive_demo()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting interactive demo.")


if __name__ == "__main__":
    main()
