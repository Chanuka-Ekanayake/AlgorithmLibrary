import sys
import time
from pathlib import Path
from collections import Counter

# Add parent directory for core logic
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

try:
    from core.reservoir import ReservoirSampler
except ImportError:
    print("Error: Ensure 'core/reservoir.py' and 'core/__init__.py' exist.")
    sys.exit(1)

def run_fairness_test():
    """
    Runs the sampler many times on a small stream and checks if the 
    distribution of selected items is roughly uniform.
    """
    print("=" * 65)
    print("SYSTEM: RANDOMIZED SAMPLING ENGINE")
    print("ALGORITHM: RESERVOIR SAMPLING (ALGORITHM R)")
    print("=" * 65 + "\n")

    # Parameters
    STREAM_SIZE = 100
    K = 10
    TRIALS = 10000
    
    print(f"[TEST] Stream size: {STREAM_SIZE}")
    print(f"[TEST] Reservoir size (k): {K}")
    print(f"[TEST] Running {TRIALS} trials to check fairness...\n")

    # We use a stream of numbers 0..99
    stream = list(range(STREAM_SIZE))
    counts = Counter()

    start = time.perf_counter()
    for _ in range(TRIALS):
        sample = ReservoirSampler.sample_from_iterable(stream, K)
        for item in sample:
            counts[item] += 1
    end = time.perf_counter()

    # Calculation
    # Expected count for each item = (TRIALS * K) / STREAM_SIZE
    expected = (TRIALS * K) / STREAM_SIZE
    
    print(f"[LOG] Execution time: {(end - start) * 1000:.2f} ms")
    print(f"[LOG] Expected frequency per item: {expected}\n")

    # Sample some frequencies
    print("Detailed frequencies for first 5 items:")
    for i in range(5):
        actual = counts[i]
        diff = ((actual - expected) / expected) * 100
        print(f"  Item {i}: {actual} (Deviation: {diff:+.2f}%)")

    print("\nDetailed frequencies for last 5 items:")
    for i in range(STREAM_SIZE - 5, STREAM_SIZE):
        actual = counts[i]
        diff = ((actual - expected) / expected) * 100
        print(f"  Item {i}: {actual} (Deviation: {diff:+.2f}%)")

    # Summary Stats (include items that never appeared by iterating over full range)
    max_freq = max(counts[i] for i in range(STREAM_SIZE))
    min_freq = min(counts[i] for i in range(STREAM_SIZE))
    max_dev = ((max_freq - expected) / expected) * 100
    min_dev = ((min_freq - expected) / expected) * 100

    print("\n" + "=" * 65)
    print("STATISTICAL REPORT")
    print("=" * 65)
    print(f"  Average frequency : {sum(counts[i] for i in range(STREAM_SIZE)) / STREAM_SIZE}")
    print(f"  Max frequency     : {max_freq} ({max_dev:+.2f}%)")
    print(f"  Min frequency     : {min_freq} ({min_dev:+.2f}%)")
    print("-" * 65)
    
    if abs(max_dev) < 10 and abs(min_dev) < 10:
        print("RESULT: PASS - Distribution is statistically uniform.")
    else:
        print("RESULT: FAIL - Distribution appears biased. Check PRNG.")
    print("=" * 65)

def run_streaming_demo():
    """Demonstrates use of the generator interface."""
    print("\n[DEMO] Using the generator (streaming) interface...")
    
    sampler_gen = ReservoirSampler.streaming_sample(k=3, seed=42)
    next(sampler_gen) # Prime the generator
    
    # Simulate a live stream
    live_stream = ["Apple", "Banana", "Cherry", "Date", "Elderberry", "Fig", "Grape"]
    
    for fruit in live_stream:
        reservoir = sampler_gen.send(fruit)
        print(f"  Received: {fruit:<10} | Current Reservoir: {reservoir}")

if __name__ == "__main__":
    run_fairness_test()
    run_streaming_demo()
