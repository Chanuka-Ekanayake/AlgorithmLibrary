# Aho-Corasick Multi-Pattern Matching

## 1. Overview

The **Aho-Corasick algorithm** is the gold standard for simultaneously searching a text for multiple patterns. It builds a **finite-state automaton** from a dictionary of K patterns in **O(M)** time (M = total pattern length), then scans any text of length N in **O(N + Z)** time — where Z is the total number of matches — regardless of how many patterns exist.

Running K separate KMP searches would cost O(K × N). Aho-Corasick removes that linear factor in K entirely: the text is read **exactly once**, and every pattern is matched simultaneously in that single pass.

---

## 2. Technical Features

- **O(M) Construction:** One-time trie insertion for all patterns, followed by a single BFS to compute failure links. No per-text preprocessing required.
- **O(N + Z) Search:** Each text character triggers at most one forward transition. Failure-link jumps are amortised O(1) per character; O(N) total for the full text.
- **Output Link Inheritance:** During BFS, each node inherits its failure-link's outputs. This ensures O(1) match reporting per character position — no chain-following at search time.
- **Overlapping Matches:** Correctly detects patterns that overlap positionally (e.g., `"he"` and `"she"` both matched in `"ushers"`).
- **Convenience API:** `search` (all matches), `first_match` (earliest hit), `contains_any` (short-circuit boolean), `count_matches` (total occurrences).

---

## 3. Architecture

```text
.
├── core/                           # Aho-Corasick Automaton Engine
│   ├── __init__.py                 # Package initialisation
│   └── aho_corasick.py            # Trie, BFS failure links, text search
├── docs/                           # Technical Documentation
│   ├── logic.md                    # Trie construction, failure links, search walkthrough
│   └── complexity.md               # Full complexity proof and comparison table
├── test-project/                   # Network IDS Simulator
│   ├── app.py                      # Multi-packet scan demo with threat classification
│   └── instructions.md             # Guide for running and interpreting the simulator
└── README.md                       # Documentation Entry Point
```

---

## 4. Performance Specifications

| Metric                     | Specification                                                           |
|----------------------------|-------------------------------------------------------------------------|
| **Automaton Construction** | O(M) — trie insertion + BFS failure-link computation                   |
| **Text Search**            | O(N + Z) — single left-to-right pass; Z = total match count            |
| **Space**                  | O(M × Σ) — M trie nodes; Σ = alphabet size (dict uses only seen chars)|
| **Overlapping Matches**    | Fully supported via output-link inheritance                             |

---

## 5. Deployment & Usage

### Integration

```python
from core.aho_corasick import AhoCorasick

# Build the automaton once — O(M)
ac = AhoCorasick(["he", "she", "his", "hers"])

# Search any number of texts — O(N + Z) each
matches = ac.search("ushers")
for start, end, pattern in matches:
    print(f"  '{pattern}' found at [{start}:{end}]")
# Output:
#   'she' found at [1:4]
#   'he'  found at [2:4]
#   'hers' found at [2:6]

# Short-circuit boolean check
if ac.contains_any("his name is here"):
    print("At least one pattern found!")

# Count total occurrences
n = ac.count_matches("she sells seashells")
print(f"Total matches: {n}")
```

### Running the IDS Simulator

1. Navigate to the `test-project` directory:

```bash
cd test-project
```

2. Run the Network Intrusion Detection Engine:

```bash
python app.py
```

---

## 6. Industrial Applications

- **Network Intrusion Detection:** Snort, Suricata, and other IDS engines use Aho-Corasick to scan each packet against tens of thousands of attack signatures in microseconds.
- **Antivirus Scanners:** ClamAV's pattern matching engine is built on Aho-Corasick for scanning files against a malware signature database.
- **Spam Filtering:** Email spam filters simultaneously check message bodies against thousands of known spam phrases in a single text pass.
- **DNA Sequence Analysis:** Searching a genome for a panel of short probe sequences (e.g., CRISPR off-target sites) simultaneously instead of running K separate scans.
- **Log Analysis:** SIEM systems (Splunk, Elastic) use multi-pattern matching to detect security-relevant keywords across high-volume log streams.
- **Web Application Firewalls (WAF):** ModSecurity rule engines scan HTTP request/response bodies for injection patterns, XSS payloads, and known exploit strings.
