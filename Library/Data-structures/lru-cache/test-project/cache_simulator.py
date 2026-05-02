#!/usr/bin/env python3
"""
Cache Simulator: Interactive demonstration of LRU Cache behavior.

This tool helps visualize how the LRU Cache evicts items and manages capacity.
"""

import sys
from pathlib import Path

# Add parent directory to path to import the core module
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.lru_cache import LRUCache


class CacheSimulator:
    """Interactive cache simulator for educational purposes."""
    
    def __init__(self, capacity: int):
        """Initialize the simulator with a given cache capacity."""
        self.cache = LRUCache(capacity)
        self.operation_log = []
    
    def display_status(self):
        """Display current cache status."""
        stats = self.cache.get_stats()
        print("\n" + "="*60)
        print(f"CACHE STATUS")
        print("="*60)
        print(f"Capacity: {stats['capacity']}")
        print(f"Current Size: {stats['current_size']}")
        print(f"Occupancy Rate: {stats['occupancy_rate']*100:.1f}%")
        print(f"Items (oldest → newest): {stats['keys_in_order']}")
        print("="*60 + "\n")
    
    def log_operation(self, operation: str, key: str, result: str):
        """Log an operation for the history."""
        self.operation_log.append({
            'operation': operation,
            'key': key,
            'result': result
        })
    
    def display_history(self):
        """Display operation history."""
        print("\n" + "="*60)
        print(f"OPERATION HISTORY ({len(self.operation_log)} ops)")
        print("="*60)
        for i, log in enumerate(self.operation_log[-10:], 1):  # Show last 10
            print(f"{i}. {log['operation']:10} key={log['key']:10} → {log['result']}")
        print("="*60 + "\n")
    
    def run_interactive(self):
        """Run interactive mode."""
        print("\n" + "="*60)
        print("LRU CACHE SIMULATOR - Interactive Mode")
        print("="*60)
        print(f"Initial capacity: {self.cache.capacity}")
        print("\nCommands:")
        print("  put <key> <value>    - Add/update item")
        print("  get <key>            - Retrieve item")
        print("  delete <key>         - Remove item")
        print("  status               - Show cache status")
        print("  history              - Show operation history")
        print("  demo                 - Run automated demo")
        print("  exit                 - Exit simulator")
        print("="*60 + "\n")
        
        while True:
            try:
                command = input(">>> ").strip().split()
                
                if not command:
                    continue
                
                cmd = command[0].lower()
                
                if cmd == "put" and len(command) >= 3:
                    key = command[1]
                    value = " ".join(command[2:])
                    self.cache.put(key, value)
                    self.log_operation("PUT", key, f"stored '{value}'")
                    self.display_status()
                
                elif cmd == "get" and len(command) >= 2:
                    key = command[1]
                    result = self.cache.get(key)
                    self.log_operation("GET", key, f"found '{result}'" if result is not None else "NOT FOUND")
                    self.display_status()
                
                elif cmd == "delete" and len(command) >= 2:
                    key = command[1]
                    deleted = self.cache.delete(key)
                    self.log_operation("DELETE", key, "removed" if deleted else "not found")
                    self.display_status()
                
                elif cmd == "status":
                    self.display_status()
                
                elif cmd == "history":
                    self.display_history()
                
                elif cmd == "demo":
                    self.run_demo()
                
                elif cmd == "exit":
                    print("Exiting simulator...")
                    break
                
                else:
                    print("Invalid command. Try 'help' for usage.")
            
            except KeyboardInterrupt:
                print("\n\nExiting simulator...")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def run_demo(self):
        """Run automated demonstration."""
        print("\n" + "="*60)
        print("RUNNING AUTOMATED DEMO")
        print("="*60)
        
        # Scenario: User profile cache for a social app
        print("\nScenario: Caching user profiles (capacity=3)")
        self.cache = LRUCache(3)
        
        print("\n1. Adding users Alice, Bob, Charlie")
        self.cache.put("user_1", "Alice")
        self.cache.put("user_2", "Bob")
        self.cache.put("user_3", "Charlie")
        self.display_status()
        
        print("2. Accessing Alice (marks as recently used)")
        result = self.cache.get("user_1")
        print(f"   Retrieved: {result}")
        self.display_status()
        
        print("3. Adding new user David (Bob should be evicted)")
        self.cache.put("user_4", "David")
        self.display_status()
        
        print("4. Try to access Bob (should be gone)")
        result = self.cache.get("user_2")
        print(f"   Retrieved: {result}")
        self.display_status()
        
        print("5. Accessing Charlie (mark as recently used)")
        result = self.cache.get("user_3")
        print(f"   Retrieved: {result}")
        self.display_status()
        
        print("6. Adding Emma (Alice should be evicted, Charlie is most recent)")
        self.cache.put("user_5", "Emma")
        self.display_status()
        
        print("7. Final state: Cache contains David, Charlie, Emma")
        print(f"   Keys: {self.cache.get_all_keys()}")
        print("="*60 + "\n")


def main():
    """Main entry point."""
    print("\nLRU Cache Simulator")
    print("="*60)
    
    # Get capacity from user
    while True:
        try:
            capacity = int(input("Enter cache capacity (1-100): "))
            if 1 <= capacity <= 100:
                break
            print("Please enter a number between 1 and 100")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    # Create simulator
    simulator = CacheSimulator(capacity)
    
    # Ask for mode
    print("\nSelect mode:")
    print("1. Interactive (manual commands)")
    print("2. Automated Demo")
    mode = input("Enter choice (1 or 2): ").strip()
    
    if mode == "2":
        simulator.run_demo()
    else:
        simulator.run_interactive()


if __name__ == "__main__":
    main()
