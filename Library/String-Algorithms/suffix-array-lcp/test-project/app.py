import sys
import time
from pathlib import Path

# Resolve project root so imports work from any working directory
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

try:
    from core.suffix_array import SuffixArray
except ImportError:
    print("Error: Ensure 'core/suffix_array.py' and 'core/__init__.py' exist.")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Simulated Document Corpus
# ---------------------------------------------------------------------------

SUBMITTED_DOCUMENT = (
    "machine learning algorithms are transforming the software industry. "
    "deep learning models, including convolutional neural networks, rely on "
    "gradient descent optimization to minimize the loss function. "
    "machine learning is increasingly used in healthcare, finance, and robotics. "
    "the application of neural networks to image recognition has revolutionized "
    "computer vision, with deep learning achieving superhuman accuracy."
)

REFERENCE_DOCUMENT = (
    "the field of deep learning has seen rapid advances in recent years. "
    "convolutional neural networks are the backbone of modern image recognition. "
    "gradient descent and its variants power the training of these models. "
    "software engineers integrate machine learning pipelines into production systems."
)

SEARCH_QUERY = "neural networks"


def separator(char: str = "-", width: int = 68) -> None:
    print(char * width)


def run_plagiarism_detector() -> None:
    separator("=")
    print("SYSTEM: PLAGIARISM DETECTION ENGINE")
    print("ALGORITHM: SUFFIX ARRAY + LCP ARRAY")
    separator("=")
    print()

    # ------------------------------------------------------------------
    # Step 1: Build the Suffix Array for the submitted document
    # ------------------------------------------------------------------
    print(f"[DATA] Submitted document length : {len(SUBMITTED_DOCUMENT)} characters")
    print(f"[DATA] Reference document length : {len(REFERENCE_DOCUMENT)} characters")
    print()

    print("[PROCESSING] Building Suffix Array for submitted document...")
    t0 = time.perf_counter()
    sa_obj = SuffixArray(SUBMITTED_DOCUMENT)
    t1 = time.perf_counter()
    build_ms = (t1 - t0) * 1000

    print(f"[OK] Suffix Array built in {build_ms:.4f} ms  (O(N log N))")
    print(f"     Total suffixes indexed: {len(sa_obj.sa)}")
    separator()
    print()

    # ------------------------------------------------------------------
    # Step 2: Pattern Search — O(M log N)
    # ------------------------------------------------------------------
    print(f"[QUERY] Searching for pattern: \"{SEARCH_QUERY}\"")
    t0 = time.perf_counter()
    positions = sa_obj.search(SEARCH_QUERY)
    t1 = time.perf_counter()
    search_ms = (t1 - t0) * 1000

    print()
    separator("=")
    print("SEARCH REPORT")
    separator("=")
    print(f"Pattern         : \"{SEARCH_QUERY}\"")
    print(f"Occurrences     : {len(positions)}")
    print(f"Query Time      : {search_ms:.4f} ms  (O(M log N))")
    print()

    for i, pos in enumerate(positions, 1):
        start = max(0, pos - 20)
        end = min(len(SUBMITTED_DOCUMENT), pos + len(SEARCH_QUERY) + 20)
        snippet = SUBMITTED_DOCUMENT[start:end].replace("\n", " ")
        print(f"  Match {i} at index {pos:<4} | \"...{snippet}...\"")

    separator()
    print()

    # ------------------------------------------------------------------
    # Step 3: Longest Repeated Substring — O(N)
    # ------------------------------------------------------------------
    print("[PROCESSING] Finding longest repeated substring in submitted document...")
    t0 = time.perf_counter()
    lrs = sa_obj.longest_repeated_substring()
    t1 = time.perf_counter()
    lrs_ms = (t1 - t0) * 1000

    print()
    separator("=")
    print("LONGEST REPEATED SUBSTRING REPORT")
    separator("=")
    print(f"Result   : \"{lrs}\"")
    print(f"Length   : {len(lrs)} characters")
    print(f"Time     : {lrs_ms:.4f} ms  (O(N) LCP scan)")
    separator()
    print()

    # ------------------------------------------------------------------
    # Step 4: Longest Common Substring — O((N+M) log(N+M))
    # ------------------------------------------------------------------
    print("[PROCESSING] Comparing submitted vs reference document...")
    t0 = time.perf_counter()
    lcs = sa_obj.longest_common_substring(REFERENCE_DOCUMENT)
    t1 = time.perf_counter()
    lcs_ms = (t1 - t0) * 1000

    print()
    separator("=")
    print("LONGEST COMMON SUBSTRING REPORT (PLAGIARISM SIGNAL)")
    separator("=")
    print(f"Shared substring : \"{lcs}\"")
    print(f"Length           : {len(lcs)} characters")
    print(f"Time             : {lcs_ms:.4f} ms  (O((N+M) log(N+M)))")
    separator()
    print()

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    separator("=")
    print("EXECUTION SUMMARY")
    separator("=")
    total_ms = build_ms + search_ms + lrs_ms + lcs_ms
    print(f"  SA Build (O(N log N))       : {build_ms:.4f} ms")
    print(f"  Pattern Search (O(M log N)) : {search_ms:.4f} ms")
    print(f"  LRS Detection (O(N))        : {lrs_ms:.4f} ms")
    print(f"  LCS Detection               : {lcs_ms:.4f} ms")
    print(f"  Total                       : {total_ms:.4f} ms")
    separator("=")
    print("RESULT: Plagiarism analysis complete using Suffix Array + LCP.")
    separator("=")


if __name__ == "__main__":
    run_plagiarism_detector()
