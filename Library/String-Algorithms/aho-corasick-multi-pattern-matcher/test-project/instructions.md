# Running the Aho-Corasick IDS Simulator

This test project simulates a **Network Intrusion Detection System (IDS)** that scans raw packet payloads against a dictionary of known attack signatures using the Aho-Corasick automaton.

## Steps

1. Navigate to the `test-project` directory:

```bash
cd test-project
```

2. Run the IDS simulator:

```bash
python app.py
```

## What to Observe

- **Automaton Build Time** — how long O(M) construction takes for the full signature dictionary.
- **Per-Packet Scan Time** — each packet is scanned in O(N + Z); observe near-constant time regardless of signature count.
- **Match Reports** — every matching signature is reported with its byte offset and surrounding context snippet.
- **Quick Triage** — the `contains_any` helper stops at first match, useful for packet drop decisions in real IDS pipelines.
- **Threat vs. Clean Classification** — packets P-001, P-002, P-004, P-005 should be flagged; P-003 should be clean.
