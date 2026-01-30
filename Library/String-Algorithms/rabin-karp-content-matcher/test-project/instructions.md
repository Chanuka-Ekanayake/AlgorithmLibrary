# User Guide: Malware Signature Scanner (Rabin-Karp)

This project demonstrates how rolling hashes are used for high-speed content security.

## How it Works
The `RabinKarp` engine calculates a unique numerical "fingerprint" for every malicious signature in `library.txt`. It then slides a window over the target code, checking fingerprints in $O(1)$ time. This allows us to search for many patterns at once without slowing down the scan.

## Instructions
1. Navigate to the `test-project` directory.
2. Run the scanner:
   ```bash
   python app.py