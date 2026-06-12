# Running the API Shield Simulator

This simulator demonstrates the difference between the Sliding Window Counter rate limiter and traditional fixed window/bucket limiters, displaying request intercepts in real time.

### 1. Execution

Run the simulator using Python:
```bash
python app.py
```

### 2. What to Audit in the Output

* **Scenario 1 (Spam Attack):** See how a user attempting to send 10 rapid-fire requests is immediately limited after the 5th request.
* **Scenario 2 (Decay & Refill):** Notice how the sliding window count slowly decays and allows a single request as time passes, demonstrating the rolling window behavior.
* **Scenario 3 (Smooth Boundary):** Observe the system keeping a stable, strict rate limit without allowing bursts at fixed interval boundaries.
