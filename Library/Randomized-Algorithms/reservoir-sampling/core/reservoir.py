"""
Reservoir Sampling
Implements the classic Algorithm R for uniformly sampling k items from a 
stream of unknown or infinite size in a single pass.

This is a fundamental randomized algorithm for streaming data, ensuring that 
at any point in the stream, every item seen so far has an equal probability
of being in the reservoir.
"""

import random
from typing import List, Iterable, Any, TypeVar

T = TypeVar('T')

class ReservoirSampler:
    """
    A sampler that maintains a representative sample (reservoir) of a stream.
    
    This implementation uses Algorithm R (Vitter, 1985).
    """

    @staticmethod
    def sample_from_iterable(iterable: Iterable[T], k: int, seed: int = None) -> List[T]:
        """
        Samples k items from an iterable in a single pass.
        
        Args:
            iterable: A stream of items (can be a list, generator, etc.)
            k: The number of items to sample.
            seed: Optional random seed for reproducibility.
            
        Returns:
            A list containing k items sampled uniformly from the iterable.
            If the iterable has fewer than k items, all items are returned.
        """
        if k <= 0:
            return []

        rng = random.Random(seed)
        reservoir: List[T] = []
        
        # 1. Fill the reservoir with the first k items
        iterator = iter(iterable)
        try:
            for _ in range(k):
                reservoir.append(next(iterator))
        except StopIteration:
            # Iterable had fewer than k items
            return reservoir

        # 2. For every subsequent item, replace an existing item in the 
        #    reservoir with decreasing probability.
        #    The i-th item (0-indexed) has a k/(i+1) chance of being selected.
        for i, item in enumerate(iterator, start=k):
            j = rng.randint(0, i)
            if j < k:
                reservoir[j] = item
                
        return reservoir

    @staticmethod
    def streaming_sample(k: int, seed: int = None):
        """
        A stateful sampler that can process items one by one.
        Useful for extremely long-running streams where items arrive over time.
        
        Usage:
            sampler = ReservoirSampler.streaming_sample(k=10)
            next(sampler) # Initialize
            for item in huge_stream:
                reservoir = sampler.send(item)
        """
        rng = random.Random(seed)
        reservoir: List[Any] = []
        count = 0
        
        while True:
            item = yield reservoir
            count += 1
            
            if len(reservoir) < k:
                reservoir.append(item)
            else:
                j = rng.randint(0, count - 1)
                if j < k:
                    reservoir[j] = item
