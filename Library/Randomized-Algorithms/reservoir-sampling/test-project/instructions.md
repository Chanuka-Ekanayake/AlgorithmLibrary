# User Guide: Streaming Sample Engine (Reservoir Sampling)

This project demonstrates **Reservoir Sampling** (Algorithm R). It includes a statistical fairness test to prove the algorithm's uniformity and a live-stream demo showing how to use the generator interface.

## How to Test

1. **Navigate** to the `test-project` folder.
2. **Run** the simulator:
   ```bash
   python app.py
   ```

## What to Observe

### 1. Statistical Uniformity
The script runs 10,000 trials of sampling from a stream of 100 items. 
- **Expected Frequency:** Every item should ideally appear exactly `(Trials * K) / N` times.
- **Verification:** The "Statistical Report" checks if the actual counts stay within a small deviation from the expected value.

### 2. Live Stream Update
The second part of the script shows the reservoir updating in real-time as items are "sent" to the generator. Notice how:
- The first 3 items are always kept.
- Subsequent items replace existing ones probabilistically.

## Experimentation

Change these values in `app.py` to see different results:
- `TRIALS`: Increase for higher statistical confidence (but slower runtime).
- `K`: Number of items to pick.
- `STREAM_SIZE`: Total pool of items to sample from.
