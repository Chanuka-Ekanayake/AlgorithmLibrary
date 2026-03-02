import sys
import time
from pathlib import Path

# Add parent directory for core logic
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

try:
    from core.network import DinicMaxFlow
except ImportError:
    print("Error: Ensure 'core/network.py' and 'core/__init__.py' exist.")
    sys.exit(1)

def run_cdn_simulator():
    print("-" * 65)
    print("SYSTEM: GLOBAL CDN BANDWIDTH ROUTER")
    print("ENGINE: DINIC'S MAXIMUM FLOW ALGORITHM")
    print("-" * 65 + "\n")

    # 1. Define the CDN Topology
    # Node 0: Main Datacenter (Source)
    # Node 1: Edge Server (US-East)
    # Node 2: Edge Server (US-West)
    # Node 3: Edge Server (EU-Central)
    # Node 4: Edge Server (Asia-East)
    # Node 5: Buyer's Machine (Sink)
    num_servers = 6
    cdn = DinicMaxFlow(num_servers)
    
    source = 0
    sink = 5

    print(f"[NETWORK] Initializing CDN with {num_servers} nodes...")
    print("[NETWORK] Provisioning fiber-optic links (Capacities in Gbps):")

    # Connections from Datacenter to Tier 1 Edge Servers
    cdn.add_edge(0, 1, 16.0)  # Datacenter -> US-East (16 Gbps)
    cdn.add_edge(0, 2, 13.0)  # Datacenter -> US-West (13 Gbps)
    print("  ├─ Datacenter -> US-East: 16.0 Gbps")
    print("  ├─ Datacenter -> US-West: 13.0 Gbps")

    # Cross-connections between Edge Servers
    cdn.add_edge(1, 2, 10.0)  # US-East -> US-West
    cdn.add_edge(2, 1, 4.0)   # US-West -> US-East
    cdn.add_edge(1, 3, 12.0)  # US-East -> EU-Central
    cdn.add_edge(2, 4, 14.0)  # US-West -> Asia-East
    cdn.add_edge(3, 2, 9.0)   # EU-Central -> US-West
    cdn.add_edge(4, 3, 7.0)   # Asia-East -> EU-Central
    print("  ├─ Inter-Edge Routing Links Provisioned")

    # Connections from Edge Servers to the Buyer
    cdn.add_edge(3, 5, 20.0)  # EU-Central -> Buyer
    cdn.add_edge(4, 5, 4.0)   # Asia-East -> Buyer
    print("  ├─ EU-Central -> Buyer: 20.0 Gbps")
    print("  └─ Asia-East -> Buyer: 4.0 Gbps\n")

    # 2. Execute Dinic's Algorithm
    print("[PROCESSING] Calculating Maximum Theoretical Throughput...")
    start_time = time.perf_counter()
    
    max_bandwidth = cdn.calculate_max_flow(source, sink)
    
    end_time = time.perf_counter()

    # 3. Output Results
    print("\n" + "=" * 65)
    print("CDN THROUGHPUT REPORT")
    print("=" * 65)
    print(f"Max Download Speed: {max_bandwidth:.2f} Gbps")
    
    # Contextualizing the speed for the e-commerce platform
    model_size_gb = 50.0 # 50 Gigabyte ML Model
    # Convert Gbps (Gigabits) to GBps (Gigabytes) by dividing by 8
    download_time_seconds = model_size_gb / (max_bandwidth / 8.0)
    
    print(f"Platform Metric:    A 50 GB Machine Learning Model will")
    print(f"                    download in exactly {download_time_seconds:.2f} seconds.")
    print("-" * 65)
    print(f"Engine Exec Time:   {(end_time - start_time) * 1000:.4f} ms")
    print("=" * 65)

if __name__ == "__main__":
    run_cdn_simulator()