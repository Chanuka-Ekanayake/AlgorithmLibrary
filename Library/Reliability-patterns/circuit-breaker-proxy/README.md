# Circuit Breaker Pattern (Reliability Proxy)

## 1. Overview

The **Circuit Breaker** is a critical stability pattern used in modern distributed systems to prevent **cascading failures**. In a microservice architecture, if one service (like an ML inference engine or payment gateway) becomes slow or fails, a "ripple effect" can occur where the calling service exhausts its own resources waiting for a response, eventually crashing the entire platform.

The Circuit Breaker wraps these dangerous calls in a state machine. If failures exceed a certain threshold, the circuit "trips," immediately failing all subsequent calls for a set period. This provides the failing service "breathing room" to recover and protects the rest of the system's integrity.

---

## 2. Technical Features

- **Finite State Machine (FSM):** Operates in three distinct modes: `CLOSED` (healthy), `OPEN` (protecting), and `HALF_OPEN` (testing).
- **Fail-Fast Mechanism:** When the circuit is open, requests are rejected immediately, bypassing the network and saving thread/memory resources.
- **Automatic Recovery:** Uses a time-based decay logic to transition from `OPEN` to `HALF_OPEN`, allowing the system to self-heal without manual intervention.
- **Tunable Sensitivity:** Configurable `failure_threshold` and `recovery_timeout` parameters to balance between system protection and service availability.

---

## 3. Architecture

```text
.
├── core/                  # Reliability Engine
│   ├── __init__.py        # Package initialization
│   └── circuit_breaker.py # State machine logic and exception handling
├── docs/                  # Technical Documentation
│   ├── logic.md           # State transition diagrams and recovery theory
│   └── complexity.md      # Analysis of O(1) overhead and MTTR impact
├── test-project/          # Stability Simulator
│   ├── app.py             # Real-time simulation of a "flaky" ML API
│   └── instructions.md    # Guide for auditing self-healing behavior
└── README.md              # Documentation Entry Point

```

---

## 4. Performance Specifications

| Metric                 | Specification                               |
| ---------------------- | ------------------------------------------- |
| **Execution Overhead** | (Constant time state checks)                |
| **Space Complexity**   | (Fixed memory per instance)                 |
| **Latency Impact**     | Zero (Checks occur in nanoseconds)          |
| **Fault Isolation**    | High (Prevents service-wide collapse)       |
| **Protocol Support**   | Language/Protocol agnostic (REST, gRPC, DB) |

---

## 5. Deployment & Usage

### Integration

The `CircuitBreaker` can be used to wrap any flaky network or database call within your marketplace backend:

```python
from core.circuit_breaker import CircuitBreaker

# Trip after 5 failures, wait 30 seconds to retry
breaker = CircuitBreaker(failure_threshold=5, recovery_timeout=30.0)

def call_unstable_service():
    # Your network request here...
    pass

# Execute with protection
try:
    response = breaker.call(call_unstable_service)
except Exception as e:
    # Handle the "Fail-Fast" rejection or the actual service error
    print(f"System protected: {e}")

```

### Running the Simulator

To observe the circuit breaker detecting failures and automatically healing in a live environment:

1. Navigate to the `test-project` directory:

```bash
cd test-project

```

2. Run the Stability Simulator:

```bash
python app.py

```

---

## 6. Industrial Applications

- **Microservice Resiliency:** Standard practice in Netflix (Hystrix), Amazon, and Google architectures.
- **Third-Party API Guard:** Protecting your app from downtime in external services (Stripe, Twilio, OpenAI).
- **Database Protection:** Preventing a "thundering herd" of queries from crushing a database that is already struggling.
- **Frontend Stability:** Ensuring a "loading" or "error" state is shown instantly rather than hanging the browser.
