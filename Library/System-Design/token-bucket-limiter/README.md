# Token Bucket Rate Limiter

## 1. Overview

The **Token Bucket** is the industry-standard algorithm for controlling the rate of incoming requests to a service or API. It provides a sophisticated balance between strictly limiting long-term throughput and allowing short-term "bursts" of traffic. This ensures that users experience a responsive interface while the underlying infrastructure remains protected from exhaustion and DDoS attacks.

---

## 2. Technical Features

- **Lazy Refill Logic:** Unlike traditional implementations that require background threads to replenish tokens, this engine uses a "Lazy Evaluation" strategy. Tokens are recalculated only at the moment of a request, reducing idle CPU usage to near zero.
- **Thread-Safe Design:** Built with atomic `threading.Lock` mechanisms, making it safe for use in multi-threaded production environments like Flask, Django, or FastAPI.
- **Burst Capacity Support:** Accommodates high-frequency bursts by allowing tokens to accumulate up to a defined maximum capacity.
- **Multi-User Management:** Includes a `RateLimitManager` to track unique buckets for thousands of individual users or IP addresses simultaneously.

---

## 3. Architecture

```text
.
├── core/                  # Engine Logic
│   ├── __init__.py        # Package initialization
│   └── rate_limiter.py    # Thread-safe Token Bucket & Manager
├── docs/                  # Technical Documentation
│   ├── logic.md           # The "Water & Bucket" analogy and refill math
│   └── complexity.md      # O(1) performance and memory scaling analysis
├── test-project/          # API Endpoint Shield
│   ├── app.py             # Tiered access simulator (Free vs. Pro)
│   └── instructions.md    # Guide for testing burst and recovery
└── README.md              # Documentation Entry Point

```

---

## 4. Performance Specifications

| Metric               | Specification                        |
| -------------------- | ------------------------------------ |
| **Check Latency**    | (Sub-millisecond)                    |
| **Memory Footprint** | (~200 bytes per active user)         |
| **Refill Strategy**  | On-Demand (Deterministic)            |
| **Paradigm**         | Traffic Shaping / Congestion Control |

---

## 5. Deployment & Usage

### Integration

The `RateLimitManager` can be integrated into your middleware to protect specific endpoints:

```python
from core.rate_limiter import RateLimitManager

# 5 tokens max, refills 1 token per second
limiter = RateLimitManager(default_capacity=5, default_refill_rate=1.0)

def handle_api_request(user_id):
    if limiter.is_allowed(user_id):
        return "200 OK", "Data retrieved."
    else:
        return "429 Too Many Requests", "Rate limit exceeded."

```

### Running the Simulator

To observe the difference between tiered users (Free vs. Pro) and see the burst logic in action:

1. Navigate to the `test-project` directory:

```bash
cd test-project

```

2. Run the shield simulation:

```bash
python app.py

```

---

## 6. Industrial Applications

- **Public APIs:** Used by providers like Stripe and AWS to enforce subscription-based usage limits.
- **Infrastructure Protection:** Preventing a single malfunctioning client or malicious bot from overwhelming a database.
- **Microservices:** Controlling the flow of communication between internal services to prevent cascading failures.
- **Cloud Scaling:** Smoothing out traffic spikes to prevent unnecessary auto-scaling of server resources.
