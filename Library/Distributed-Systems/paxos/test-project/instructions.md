# User Guide: Distributed Database Consensus (Paxos)

This project simulates the **Single-Decree Paxos** algorithm managing a 5-node distributed cluster. It demonstrates how competing servers agree on a single sequence of events despite network packet drops and concurrent write requests.

## How to Test
1. **Navigate** to the `test-project` folder.
2. **Run** the simulator:
   ```bash
   python app.py