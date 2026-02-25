"""
MapReduce Distributed Processing Engine
Simulates a Google-style MapReduce framework using multi-processing.
It orchestrates the splitting of data, parallel mapping, network shuffling, 
and parallel reducing.
"""

import collections
from concurrent.futures import ProcessPoolExecutor
from typing import Any, Callable, Dict, Iterable, List, Tuple

# Type aliases for clarity
Key = Any
Value = Any
KV = Tuple[Key, Value]
MapperFunc = Callable[[Any], Iterable[KV]]
ReducerFunc = Callable[[Key, Iterable[Value]], Any]

class MapReduceEngine:
    """
    Orchestrator for distributed data processing.
    """

    @staticmethod
    def _chunk_data(data: List[Any], num_chunks: int) -> List[List[Any]]:
        """
        Splits the massive input dataset into smaller 'shards' for worker nodes.
        """
        chunk_size = max(1, len(data) // num_chunks)
        return [data[i : i + chunk_size] for i in range(0, len(data), chunk_size)]

    @staticmethod
    def _map_worker(
        chunk: List[Any], 
        mapper: MapperFunc
    ) -> List[KV]:
        """
        Worker Node Logic: Applies the user's Map function to a data chunk.
        Running in a separate process, simulating a remote server.
        """
        results = []
        for item in chunk:
            # The mapper yields (key, value) pairs
            results.extend(mapper(item))
        return results

    @staticmethod
    def _reduce_worker(
        key: Key, 
        values: Iterable[Value], 
        reducer: ReducerFunc
    ) -> Any:
        """
        Worker Node Logic: Applies the user's Reduce function to grouped data.
        """
        return reducer(key, values)

    @classmethod
    def execute(
        cls,
        data: List[Any],
        mapper: MapperFunc,
        reducer: ReducerFunc,
        num_workers: int = 4
    ) -> Dict[Key, Any]:
        """
        Executes the full Map -> Shuffle -> Reduce pipeline.
        
        Args:
            data: The raw input data.
            mapper: Function that maps an item to (key, value) pairs.
            reducer: Function that reduces a list of values for a key.
            num_workers: Number of parallel processes to use.
            
        Returns:
            A dictionary containing the final reduced results.
        """
        print(f"[ENGINE] Spawning {num_workers} worker processes...")

        # ==========================================
        # PHASE 1: SPLIT & MAP
        # ==========================================
        # 1. Split data into chunks for each worker
        chunks = cls._chunk_data(data, num_workers)
        
        mapped_results: List[KV] = []
        
        # 2. Parallel Execution: Send chunks to worker processes
        # This simulates sending code to data on different servers.
        with ProcessPoolExecutor(max_workers=num_workers) as executor:
            # We map the '_map_worker' function over our chunks
            futures = [executor.submit(cls._map_worker, chunk, mapper) for chunk in chunks]
            
            for future in futures:
                mapped_results.extend(future.result())

        print(f"[ENGINE] Map Phase Complete. Generated {len(mapped_results)} intermediate pairs.")

        # ==========================================
        # PHASE 2: SHUFFLE (The Bottleneck)
        # ==========================================
        # In a real distributed system, this involves heavy network I/O
        # as nodes exchange data so all values for 'Key A' end up on 'Node A'.
        shuffled_data = collections.defaultdict(list)
        for key, value in mapped_results:
            shuffled_data[key].append(value)

        print(f"[ENGINE] Shuffle Phase Complete. Grouped into {len(shuffled_data)} unique keys.")

        # ==========================================
        # PHASE 3: REDUCE
        # ==========================================
        # Now we process each key's list of values in parallel.
        final_output = {}
        
        with ProcessPoolExecutor(max_workers=num_workers) as executor:
            # Submit a reduction job for each unique key
            future_to_key = {
                executor.submit(cls._reduce_worker, key, values, reducer): key
                for key, values in shuffled_data.items()
            }
            
            for future in future_to_key:
                key = future_to_key[future]
                final_output[key] = future.result()

        print("[ENGINE] Reduce Phase Complete.")
        return final_output