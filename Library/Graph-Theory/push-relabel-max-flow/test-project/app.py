import sys
import time
from pathlib import Path

# Add parent directory to path to import core package
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

try:
    from core.push_relabel import PushRelabelMaxFlow
except ImportError:
    print("Error: Ensure 'core/push_relabel.py' and 'core/__init__.py' exist.")
    sys.exit(1)


def run_pipeline_optimizer():
    print("=" * 70)
    print("SYSTEM: CLOUD MESH DATA INGESTION & PIPELINE ROUTER")
    print("ENGINE: HIGHEST-LABEL PUSH-RELABEL ALGORITHM (GOLDBERG-TARJAN)")
    print("=" * 70 + "\n")

    # Node Topology:
    # Node 0: Global API Ingestion Gateway (Source)
    # Node 1: Compute Cluster US-East (Virginia)
    # Node 2: Compute Cluster US-West (Oregon)
    # Node 3: Compute Cluster EU-Central (Frankfurt)
    # Node 4: Compute Cluster AP-East (Tokyo)
    # Node 5: Distributed Data Lake & Analytics Lakehouse (Sink)
    num_nodes = 6
    labels = {
        0: "Gateway [Source]",
        1: "Cluster US-East",
        2: "Cluster US-West",
        3: "Cluster EU-Central",
        4: "Cluster AP-East",
        5: "Data Lake [Sink]"
    }

    router = PushRelabelMaxFlow(num_nodes)
    source = 0
    sink = 5

    print(f"[*] Initializing mesh topology with {num_nodes} interconnected nodes...")
    print("[*] Provisioning fiber-mesh channel bandwidths (Capacities in Gbps):\n")

    # Ingestion Links from Source Gateway
    router.add_edge(0, 1, 16.0)
    router.add_edge(0, 2, 13.0)
    print("  |-- Gateway -> US-East:      16.0 Gbps")
    print("  |-- Gateway -> US-West:      13.0 Gbps")

    # Dense Inter-Cluster Mesh Connections
    router.add_edge(1, 2, 10.0)
    router.add_edge(2, 1, 4.0)
    router.add_edge(1, 3, 12.0)
    router.add_edge(2, 4, 14.0)
    router.add_edge(3, 2, 9.0)
    router.add_edge(4, 3, 7.0)
    print("  |-- Inter-Mesh Cross-Links:  10.0 Gbps (1->2), 4.0 Gbps (2->1)")
    print("  |-- Inter-Mesh Cross-Links:  12.0 Gbps (1->3), 14.0 Gbps (2->4)")
    print("  |-- Inter-Mesh Cross-Links:  9.0 Gbps (3->2),  7.0 Gbps (4->3)")

    # Egress Links to Central Data Lake
    router.add_edge(3, 5, 20.0)
    router.add_edge(4, 5, 4.0)
    print("  |-- EU-Central -> Data Lake: 20.0 Gbps")
    print("  +-- AP-East -> Data Lake:    4.0 Gbps\n")

    # Run Push-Relabel Algorithm
    print("[*] Executing Push-Relabel Max Flow Engine...")
    start_time = time.perf_counter()
    max_throughput = router.calculate_max_flow(source, sink)
    end_time = time.perf_counter()
    exec_time_ms = (end_time - start_time) * 1000

    # Extract Min-Cut Bottlenecks
    source_partition, sink_partition = router.get_min_cut(source)

    # Output Results
    print("\n" + "=" * 70)
    print("THROUGHPUT & BOTTLENECK ANALYSIS REPORT")
    print("=" * 70)
    print(f"Total Sustained Throughput: {max_throughput:.2f} Gbps")
    print(f"Algorithm Execution Time:   {exec_time_ms:.4f} ms")
    print("-" * 70)

    # Contextual application metrics
    daily_ingestion_tb = (max_throughput * 3600 * 24) / (8 * 1024)
    print(f"Maximum Daily Ingestion:    {daily_ingestion_tb:.2f} Terabytes / day")

    print("\n[+] Edge Bandwidth Utilization Breakdown:")
    print("  From                  To                    Flow / Cap (Gbps)   Status")
    print("  ----------------------------------------------------------------------")
    for edge in router.get_edge_flows():
        u_name = labels[edge['from']]
        v_name = labels[edge['to']]
        flow_str = f"{edge['flow']:5.1f} / {edge['capacity']:4.1f} Gbps"
        status = "[SATURATED]" if edge['saturated'] else f"({(edge['flow']/edge['capacity']*100):5.1f}% util)"
        print(f"  {u_name:<20} -> {v_name:<20} {flow_str:<18} {status}")

    print("\n[+] Minimum Cut Boundary (Structural Bottleneck):")
    source_nodes = [f"{labels[i]} (#{i})" for i in source_partition]
    sink_nodes = [f"{labels[i]} (#{i})" for i in sink_partition]
    print(f"  Source Side (S): {', '.join(source_nodes)}")
    print(f"  Sink Side   (T): {', '.join(sink_nodes)}")
    print("  Recommendation: Expanding egress lines leaving the Source Side (S)")
    print("                  will directly increase total system ingestion ceiling.")
    print("=" * 70)


if __name__ == "__main__":
    run_pipeline_optimizer()
