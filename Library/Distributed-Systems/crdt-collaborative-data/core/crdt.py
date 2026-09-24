"""
CRDT - Conflict-free Replicated Data Types
Implements state-based (CvRDT) primitives that guarantee Strong Eventual
Consistency through mathematically proven merge operations forming a
join-semilattice (commutative, associative, idempotent).
"""

import time
import uuid
from typing import Dict, Set, Tuple, Any, Optional


class GCounter:
    """
    Grow-only Counter (G-Counter).
    Each replica maintains its own local count. The global value is the
    sum of all replica counts. Merge takes the element-wise maximum.

    Use case: Distributed page-view counters, 'likes', download counts.
    """

    def __init__(self, replica_id: str):
        """
        Args:
            replica_id: Unique identifier for this replica/node.
        """
        self.replica_id = replica_id
        # State: {replica_id -> local_count}
        self.counts: Dict[str, int] = {replica_id: 0}

    def increment(self, amount: int = 1) -> None:
        """
        Increment this replica's local counter.
        Only the owning replica can increment its own slot.
        """
        if amount < 0:
            raise ValueError("G-Counter only supports non-negative increments. Use PNCounter for decrements.")
        self.counts[self.replica_id] = self.counts.get(self.replica_id, 0) + amount

    def value(self) -> int:
        """
        Returns the global counter value (sum of all replica counts).
        This is the 'query' operation of the CvRDT.
        """
        return sum(self.counts.values())

    def merge(self, other: 'GCounter') -> None:
        """
        Merge another G-Counter's state into this one.
        Takes element-wise maximum — guaranteed to be a join-semilattice.

        Mathematical properties:
          - Commutative:  merge(A, B) == merge(B, A)
          - Associative:  merge(merge(A, B), C) == merge(A, merge(B, C))
          - Idempotent:   merge(A, A) == A
        """
        all_replicas = set(self.counts.keys()) | set(other.counts.keys())
        for replica in all_replicas:
            self.counts[replica] = max(
                self.counts.get(replica, 0),
                other.counts.get(replica, 0)
            )

    def __repr__(self) -> str:
        return f"<GCounter '{self.replica_id}': value={self.value()}, state={self.counts}>"


class PNCounter:
    """
    Positive-Negative Counter (PN-Counter).
    Supports both increment and decrement by combining two G-Counters:
    one for positive increments (P) and one for negative decrements (N).
    The net value is P.value() - N.value().

    Use case: Inventory stock levels, upvote/downvote systems, bank balances.
    """

    def __init__(self, replica_id: str):
        """
        Args:
            replica_id: Unique identifier for this replica/node.
        """
        self.replica_id = replica_id
        self.p_counter = GCounter(replica_id)  # Tracks increments
        self.n_counter = GCounter(replica_id)  # Tracks decrements

    def increment(self, amount: int = 1) -> None:
        """Add to the positive counter."""
        self.p_counter.increment(amount)

    def decrement(self, amount: int = 1) -> None:
        """Add to the negative counter (effectively subtracting from the value)."""
        self.n_counter.increment(amount)

    def value(self) -> int:
        """Returns the net value: total increments minus total decrements."""
        return self.p_counter.value() - self.n_counter.value()

    def merge(self, other: 'PNCounter') -> None:
        """
        Merge by independently merging the P and N G-Counters.
        Inherits all semilattice guarantees from GCounter.merge().
        """
        self.p_counter.merge(other.p_counter)
        self.n_counter.merge(other.n_counter)

    def __repr__(self) -> str:
        return f"<PNCounter '{self.replica_id}': value={self.value()}, P={self.p_counter.value()}, N={self.n_counter.value()}>"


class LWWRegister:
    """
    Last-Writer-Wins Register (LWW-Register).
    A single-value register where concurrent writes are resolved by
    timestamp: the write with the highest timestamp always wins.

    Use case: User profile fields, configuration settings, status indicators.
    """

    def __init__(self, replica_id: str):
        """
        Args:
            replica_id: Unique identifier for this replica/node.
        """
        self.replica_id = replica_id
        self.value_data: Any = None
        self.timestamp: float = 0.0

    def set(self, value: Any, timestamp: Optional[float] = None) -> None:
        """
        Set the register value. Uses current wall-clock time if no
        timestamp is provided.

        Args:
            value: The new value to store.
            timestamp: Optional explicit timestamp (for deterministic testing).
        """
        ts = timestamp if timestamp is not None else time.time()
        if ts >= self.timestamp:
            self.value_data = value
            self.timestamp = ts

    def get(self) -> Any:
        """Returns the current register value."""
        return self.value_data

    def merge(self, other: 'LWWRegister') -> None:
        """
        Merge by keeping the value with the highest timestamp.
        Ties are broken by replica_id lexicographic order for determinism.
        """
        if other.timestamp > self.timestamp:
            self.value_data = other.value_data
            self.timestamp = other.timestamp
        elif other.timestamp == self.timestamp and other.replica_id > self.replica_id:
            # Deterministic tie-breaking: higher replica_id wins
            self.value_data = other.value_data
            self.timestamp = other.timestamp

    def __repr__(self) -> str:
        return f"<LWWRegister '{self.replica_id}': value={self.value_data!r}, ts={self.timestamp:.4f}>"


class ORSet:
    """
    Observed-Remove Set (OR-Set).
    A set that supports both add and remove operations with conflict-free
    semantics. Each element is tagged with a unique identifier on addition.
    Remove only removes the tags that the removing replica has *observed*.
    Concurrent adds of the same element by different replicas produce
    different tags, so 'add wins' over concurrent 'remove'.

    Use case: Collaborative shopping lists, shared playlists, user permission sets.
    """

    def __init__(self, replica_id: str):
        """
        Args:
            replica_id: Unique identifier for this replica/node.
        """
        self.replica_id = replica_id
        # State: element -> set of unique tags
        # Each tag represents one 'add' operation.
        self.elements: Dict[Any, Set[str]] = {}
        # Tombstone: set of tags that have been removed.
        self.tombstones: Set[str] = set()

    def _generate_tag(self) -> str:
        """Generate a globally unique tag for an add operation."""
        return f"{self.replica_id}:{uuid.uuid4().hex[:8]}"

    def add(self, element: Any) -> None:
        """
        Add an element with a fresh unique tag.
        Even if the element already exists, a new tag is created.
        This ensures that concurrent add + remove results in the
        element surviving (add-wins semantics).
        """
        tag = self._generate_tag()
        if element not in self.elements:
            self.elements[element] = set()
        self.elements[element].add(tag)

    def remove(self, element: Any) -> None:
        """
        Remove an element by moving all its currently observed tags
        to the tombstone set. Only tags visible to THIS replica at
        THIS moment are removed — concurrent adds from other replicas
        will have different tags and survive.
        """
        if element in self.elements:
            # Move all observed tags to tombstones
            self.tombstones |= self.elements[element]
            del self.elements[element]

    def contains(self, element: Any) -> bool:
        """Check if an element is in the set (has at least one live tag)."""
        return element in self.elements and len(self.elements[element]) > 0

    def items(self) -> set:
        """Returns the set of all live elements."""
        return {elem for elem, tags in self.elements.items() if len(tags) > 0}

    def merge(self, other: 'ORSet') -> None:
        """
        Merge another OR-Set's state into this one.

        Algorithm:
          1. Union the tombstone sets.
          2. For each element, union the tag sets from both replicas.
          3. Remove any tags that appear in the merged tombstone set.
          4. Clean up elements with no remaining live tags.

        This implements the 'add-wins' policy: a tag created by a
        concurrent add on another replica will NOT be in our tombstones,
        so it survives — the element stays in the set.
        """
        # 1. Merge tombstones
        merged_tombstones = self.tombstones | other.tombstones

        # 2. Union all element -> tag mappings
        all_elements: Dict[Any, Set[str]] = {}
        for elem, tags in self.elements.items():
            all_elements[elem] = set(tags)
        for elem, tags in other.elements.items():
            if elem in all_elements:
                all_elements[elem] |= tags
            else:
                all_elements[elem] = set(tags)

        # 3. Remove tombstoned tags
        for elem in list(all_elements.keys()):
            all_elements[elem] -= merged_tombstones
            # 4. Clean up empty entries
            if not all_elements[elem]:
                del all_elements[elem]

        self.elements = all_elements
        self.tombstones = merged_tombstones

    def __repr__(self) -> str:
        return f"<ORSet '{self.replica_id}': {self.items()}>"
