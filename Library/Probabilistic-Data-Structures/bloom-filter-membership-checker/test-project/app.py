import sys
import os
import csv
import time

# Add the parent directory to the path to import the core logic
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.bloom_filter import BloomFilter

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def security_simulation():
    clear_screen()
    print("--------------------------------------------------")
    print("SYSTEM: SECURITY PERIMETER GUARD (BLOOM FILTER)")
    print("STATUS: INITIALIZING MALICIOUS URL FILTER")
    print("--------------------------------------------------\n")

    # 1. Initialize Bloom Filter
    # Expected: 100 items with a 1% (0.01) false positive rate
    url_filter = BloomFilter(expected_items=100, false_positive_rate=0.01)

    # 2. Populate the filter from the CSV database
    try:
        with open('url_database.csv', mode='r') as file:
            reader = csv.DictReader(file)
            count = 0
            for row in reader:
                url_filter.add(row['url_string'])
                count += 1
        print(f"SUCCESS: Synced {count} known threats into memory.")
        print(f"METRICS: Bit-array size: {url_filter.size} bits.")
        print(f"METRICS: Hash functions in use: {url_filter.hash_count}\n")
    except FileNotFoundError:
        print("ERROR: url_database.csv not found.")
        return

    # 3. Interactive Membership Check
    print("Enter a URL to check its safety status (or 'exit' to quit):")
    
    while True:
        user_url = input("\nCheck URL > ").strip()
        
        if user_url.lower() == 'exit':
            break

        start_time = time.perf_counter()
        is_malicious = url_filter.exists(user_url)
        latency = (time.perf_counter() - start_time) * 1000000 # Microseconds

        if is_malicious:
            print(f"⚠️  WARNING: URL '{user_url}' is POSSIBLY MALICIOUS.")
            print(f"   ACTION: Blocking request and initiating deep database scan.")
        else:
            print(f"✅ SAFE: URL '{user_url}' is DEFINITELY NOT in the blacklist.")
            print(f"   ACTION: Allowing traffic immediately.")
        
        print(f"   LATENCY: {latency:.2f} microseconds")

    print("\n--------------------------------------------------")
    print("SYSTEM SHUTDOWN: SECURITY GUARD OFFLINE")
    print("--------------------------------------------------")

if __name__ == "__main__":
    security_simulation()