# User Guide: Database Query Accelerator

This project demonstrates the impact of **LRU Caching** on system latency.

## How it Works
1. The **MockDatabase** has a 1.5-second delay to simulate slow hardware.
2. The **LRUCache** has a capacity of **3**.
3. When you request an ID, the system checks the cache first.
4. If it's a **Miss**, it goes to the DB and "warms" the cache with the result.
5. If the cache is full (3 items), the item that hasn't been requested in the longest time is **evicted**.

## Instructions
1. Navigate to the `test-project` directory.
2. Run the application:
   ```bash
   python app.py