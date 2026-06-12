"""
Sliding Window Counter Rate Limiter
A thread-safe, memory-efficient implementation of the Sliding Window Counter algorithm.
Uses the weighted estimate approach to calculate request rate without storing timestamps.
"""

import time
from threading import Lock
from typing import Dict, Tuple

class SlidingWindowCounter:
    """
    Logic for a single Sliding Window Counter using the Weighted Estimate algorithm.
    
    Attributes:
        limit (int): The maximum number of requests allowed in the window.
        window_size (float): The sliding window duration in seconds (default: 60s).
    """
    def __init__(self, limit: int, window_size: float = 60.0):
        self.limit = limit
        self.window_size = window_size
        self.current_window_start = time.monotonic()
        self.current_count = 0
        self.previous_count = 0
        self.lock = Lock()

    def _slide_window(self, now: float) -> float:
        """
        Rotates the window counts based on elapsed time.
        Must be called under the lock.
        
        Returns:
            float: The time elapsed since the current window's start.
        """
        elapsed = now - self.current_window_start
        
        if elapsed >= self.window_size:
            # Calculate how many full window sizes have elapsed
            windows_elapsed = int(elapsed // self.window_size)
            
            if windows_elapsed == 1:
                # Exactly one window duration passed: the current count becomes the previous count
                self.previous_count = self.current_count
            else:
                # More than one window duration passed: previous count is reset to 0
                self.previous_count = 0
                
            self.current_count = 0
            # Align the start of the current window to the current boundary
            self.current_window_start += windows_elapsed * self.window_size
            elapsed = now - self.current_window_start
            
        return elapsed

    def consume(self) -> bool:
        """
        Attempts to consume 1 unit of capacity (i.e. process a single request).
        
        Returns:
            bool: True if the request is within the limit, False otherwise.
        """
        with self.lock:
            now = time.monotonic()
            elapsed = self._slide_window(now)
            
            # Calculate the weight of the previous window based on how far we are into the current one
            # As time moves forward in the current window, the previous window's weight decays.
            weight = (self.window_size - elapsed) / self.window_size
            estimated_count = (self.previous_count * weight) + self.current_count
            
            if estimated_count < self.limit:
                self.current_count += 1
                return True
            return False

    def get_status(self) -> Tuple[float, int, int]:
        """
        Calculates and returns the status of the bucket.
        
        Returns:
            Tuple[float, int, int]: (estimated_count, current_count, previous_count)
        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.current_window_start
            
            # If a lazy rotation is needed, simulate it without modifying state if not consuming,
            # or apply rotation for query consistency.
            if elapsed >= self.window_size:
                windows_elapsed = int(elapsed // self.window_size)
                prev = self.current_count if windows_elapsed == 1 else 0
                curr = 0
                elapsed_since_start = elapsed % self.window_size
            else:
                prev = self.previous_count
                curr = self.current_count
                elapsed_since_start = elapsed
                
            weight = (self.window_size - elapsed_since_start) / self.window_size
            estimated = (prev * weight) + curr
            return estimated, curr, prev


class RateLimitManager:
    """
    Manages sliding window counter buckets across multiple client identifiers (e.g. user ID, IP address).
    """
    def __init__(self, default_limit: int, default_window_size: float = 60.0):
        self.default_limit = default_limit
        self.default_window_size = default_window_size
        self.buckets: Dict[str, SlidingWindowCounter] = {}
        self.manager_lock = Lock()

    def is_allowed(self, identifier: str) -> bool:
        """
        Checks if a specific identifier is within their rate limit.
        """
        with self.manager_lock:
            bucket = self.buckets.get(identifier)
            if bucket is None:
                bucket = SlidingWindowCounter(self.default_limit, self.default_window_size)
                self.buckets[identifier] = bucket
                
        return bucket.consume()
