import sys
import time
from pathlib import Path

# Add parent directory for core logic
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

try:
    from core.analyzer import DependencyAnalyzer
except ImportError:
    print("Error: Ensure 'core/analyzer.py' and 'core/__init__.py' exist.")
    sys.exit(1)

def run_cluster_analyzer():
    print("-" * 65)
    print("SYSTEM: SOFTWARE CATALOG DEPENDENCY ANALYZER")
    print("ENGINE: KOSARAJU'S TWO-PASS SCC ALGORITHM")
    print("-" * 65 + "\n")

    # 1. Initialize the Analyzer
    analyzer = DependencyAnalyzer()

    # 2. Build the Software Catalog (Adding Dependencies)
    print("[CATALOG] Loading modules and registering dependencies...")
    
    # Valid, one-way dependencies (Safe to bundle and install)
    analyzer.add_dependency("Web-Frontend", "Auth-Service")
    analyzer.add_dependency("Auth-Service", "User-Database")
    analyzer.add_dependency("Payment-Gateway", "User-Database")
    analyzer.add_dependency("Web-Frontend", "Payment-Gateway")

    # A hidden, catastrophic Circular Dependency (The Loop)
    # ML-Engine -> Data-Pipeline -> Feature-Store -> ML-Engine
    analyzer.add_dependency("ML-Recommendation-Engine", "Data-Pipeline")
    analyzer.add_dependency("Data-Pipeline", "Feature-Store")
    analyzer.add_dependency("Feature-Store", "ML-Recommendation-Engine")
    
    # An independent valid module
    analyzer.add_dependency("Logging-Utility", "User-Database")

    print("[CATALOG] 8 modules loaded successfully.\n")

    # 3. Execute Kosaraju's Algorithm
    print("[PROCESSING] Executing Phase 1: Forward DFS (Finishing Times)...")
    print("[PROCESSING] Executing Phase 2: Reverse DFS on Transposed Graph...")
    
    start_time = time.perf_counter()
    clusters = analyzer.analyze_catalog()
    end_time = time.perf_counter()

    # 4. Output Results and Audit
    print("\n" + "=" * 65)
    print("DEPENDENCY AUDIT REPORT")
    print("=" * 65)
    
    safe_modules = 0
    fatal_errors = 0

    for idx, cluster in enumerate(clusters, 1):
        if len(cluster) == 1:
            # A cluster of 1 means it is a valid, isolated node in the topological order
            print(f"[OK]    Standalone/Valid : {cluster[0]}")
            safe_modules += 1
        else:
            # A cluster > 1 means these modules are trapped in a dependency loop
            print(f"\n[FATAL] CIRCULAR DEPENDENCY DETECTED (Cluster {idx})")
            print(f"        Modules stuck in infinite loop: {', '.join(cluster)}")
            print("        ACTION REQUIRED: Break the dependency chain before deployment.\n")
            fatal_errors += 1

    print("-" * 65)
    print(f"Audit Summary: {safe_modules} Safe Modules | {fatal_errors} Broken Clusters")
    print(f"Engine Exec Time: {(end_time - start_time) * 1000:.4f} ms")
    print("=" * 65)

if __name__ == "__main__":
    run_cluster_analyzer()