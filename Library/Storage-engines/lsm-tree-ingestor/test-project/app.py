import sys
import time
from pathlib import Path

# Add parent directory to path for core logic access
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

try:
    from core.memtable import MemTable
except ImportError:
    # Handle direct file import if core is not a package
    from core.memtable import MemTable

def run_telemetry_simulation():
    print("--------------------------------------------------")
    print("SYSTEM: HIGH-THROUGHPUT TELEMETRY LOGGER")
    print("ALGORITHM: LSM-TREE MEMTABLE (LAYER 0)")
    print("--------------------------------------------------\n")

    # Initialize a MemTable with a small threshold for demonstration
    # In production, this might be 64MB; here, we use 5 entries.
    logger = MemTable(threshold_size=5)
    
    # Simulating a stream of telemetry data from an ML model
    telemetry_events = [
        ("log_001", "Model_Inference_Success"),
        ("log_002", "Latency_25ms"),
        ("log_003", "GPU_Usage_85%"),
        ("log_004", "Memory_Alloc_2GB"),
        ("log_005", "User_ID_992_Request"), # This should trigger the first flush
        ("log_006", "Model_Inference_Success"),
        ("log_007", "Latency_22ms"),
        ("log_008", "Bias_Check_Passed"),
        ("log_009", "GPU_Usage_82%"),
        ("log_010", "User_ID_104_Request")  # This should trigger the second flush
    ]

    flush_count = 0

    for key, value in telemetry_events:
        print(f"[INGEST] Writing {key} -> {value} to Memory...")
        needs_flush = logger.put(key, value)
        
        if needs_flush:
            flush_count += 1
            print(f"\n🚀 [MEMTABLE FULL] Threshold reached ({logger.threshold_size} entries).")
            print(f"📦 [FLUSH] Preparing sorted SSTable Segment #{flush_count}...")
            
            sorted_segment = logger.flush()
            
            print("💾 [DISK] Writing sequential block to persistent storage:")
            for s_key, s_val in sorted_segment:
                print(f"   |-- {s_key}: {s_val}")
            print("✨ [CLEAN] MemTable reset and ready for new writes.\n")
            time.sleep(0.5) # Simulating slight disk I/O latency

    print("--------------------------------------------------")
    print(f"STATUS: SIMULATION COMPLETE")
    print(f"Total Flushes: {flush_count} | Total Events Logged: {len(telemetry_events)}")
    print("--------------------------------------------------")

if __name__ == "__main__":
    run_telemetry_simulation()