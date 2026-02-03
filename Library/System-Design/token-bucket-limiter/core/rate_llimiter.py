"""
Token Bucket Rate Limiter
A high-performance, thread-safe implementation of the Token Bucket algorithm.
Used for controlling the rate of requests to APIs or services.
"""

import time
from threading import Lock
from typing import Dict

class TokenBucket:
    """
    Logic for a single Token Bucket.
    
    Attributes:
        capacity (int): The maximum tokens the bucket can hold (Burst Size).
        refill_rate (float): How many tokens are added per second.
    """
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = float(capacity)
        self.refill_rate = refill_rate
        self.tokens = self.capacity
        self.last_refill_time = time.monotonic()
        self.lock = Lock()

    def _refill(self) -> None:
        """
        Calculates how many tokens should have been added since the last request.
        This 'Lazy Refill' approach avoids the need for a background thread.
        """
        now = time.monotonic()
        elapsed = now - self.last_refill_time
        
        # Calculate new tokens: (time elapsed * tokens per second)
        new_tokens = elapsed * self.refill_rate
        
        # Refill the bucket, but never exceed the capacity
        self.tokens = min(self.capacity, self.tokens + new_tokens)
        self.last_refill_time = now

    def consume(self, amount: int = 1) -> bool:
        """
        Attempts to consume a specific number of tokens.
        
        Returns:
            bool: True if tokens were available and consumed, False otherwise.
        """
        with self.lock:
            self._refill()
            
            if self.tokens >= amount:
                self.tokens -= amount
                return True
            return False

    def get_token_count(self) -> float:
        """Returns the current number of tokens in the bucket."""
        with self.lock:
            self._refill()
            return self.tokens

class RateLimitManager:
    """
    Manages multiple buckets (e.g., per-user or per-IP).
    """
    def __init__(self, default_capacity: int, default_refill_rate: float):
        self.capacity = default_capacity
        self.refill_rate = default_refill_rate
        self.buckets: Dict[str, TokenBucket] = {}
        self.manager_lock = Lock()

    def is_allowed(self, identifier: str) -> bool:
        """
        Checks if a specific identifier (User ID or IP) is within their rate limit.
        """
        with self.manager_lock:
            if identifier not in self.buckets:
                self.buckets[identifier] = TokenBucket(self.capacity, self.refill_rate)
            
        return self.buckets[identifier].consume()