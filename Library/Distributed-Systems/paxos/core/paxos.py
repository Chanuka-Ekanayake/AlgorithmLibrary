"""
Paxos Consensus Algorithm
Guarantees distributed agreement (consensus) across a cluster of independent 
nodes, even in the presence of network failures and offline servers.
"""

from typing import Any, List, Optional, Tuple
import random

class Acceptor:
    """
    Represents a database node in the distributed cluster.
    Acceptors vote on proposals and maintain strict mathematical promises 
    to never accept older, outdated proposals.
    """
    def __init__(self, node_id: int):
        self.node_id = node_id
        
        # The highest proposal ID this node has promised to listen to
        self.promised_id: int = 0
        
        # The proposal ID and value this node has definitively accepted
        self.accepted_id: int = 0
        self.accepted_value: Optional[Any] = None

    def receive_prepare(self, proposal_id: int) -> Tuple[bool, int, Optional[Any]]:
        """
        Phase 1 (Prepare): The Acceptor receives a request to vote.
        It promises to ignore any future proposals with an ID lower than this one.
        """
        if proposal_id > self.promised_id:
            self.promised_id = proposal_id
            # Return True (Promise made), along with any previously accepted data
            return (True, self.accepted_id, self.accepted_value)
        
        # Reject the proposal: A higher ID has already been promised
        return (False, self.accepted_id, self.accepted_value)

    def receive_accept(self, proposal_id: int, value: Any) -> bool:
        """
        Phase 2 (Accept): The Acceptor receives the final value to write.
        It will only accept if it hasn't made a promise to a higher ID in the meantime.
        """
        if proposal_id >= self.promised_id:
            self.promised_id = proposal_id
            self.accepted_id = proposal_id
            self.accepted_value = value
            return True
            
        return False


class Proposer:
    """
    Acts on behalf of a client trying to write data to the distributed cluster.
    Coordinates the Two-Phase commit to achieve majority consensus.
    """
    def __init__(self, proposer_id: int, acceptors: List[Acceptor]):
        self.proposer_id = proposer_id
        self.acceptors = acceptors
        self.current_proposal_id = proposer_id  # Initialize with its unique ID

    def _generate_next_proposal_id(self) -> int:
        """
        Ensures proposal IDs are unique and monotonically increasing.
        Adding the number of acceptors ensures different proposers don't generate the same ID.
        """
        self.current_proposal_id += len(self.acceptors)
        return self.current_proposal_id

    def run_consensus(self, value: Any, simulate_network_drop: float = 0.0) -> Tuple[bool, Optional[Any]]:
        """
        Executes the Paxos protocol to achieve distributed consensus.
        
        Args:
            value: The data the client wants to write.
            simulate_network_drop: Probability (0.0 to 1.0) of a message failing to simulate real-world networks.
            
        Returns:
            Tuple containing (Consensus Reached Boolean, The Final Agreed Value).
        """
        proposal_id = self._generate_next_proposal_id()
        majority = (len(self.acceptors) // 2) + 1

        # ==========================================
        # PHASE 1: PREPARE
        # ==========================================
        promises_received = 0
        highest_accepted_id = 0
        value_to_propose = value

        for acceptor in self.acceptors:
            # Simulate network packet loss
            if random.random() < simulate_network_drop:
                continue

            promised, accepted_id, accepted_val = acceptor.receive_prepare(proposal_id)
            
            if promised:
                promises_received += 1
                # CRITICAL: If an acceptor already accepted a value from a competing proposer,
                # we MUST abandon our value and adopt theirs to prevent a split-brain.
                if accepted_id > highest_accepted_id and accepted_val is not None:
                    highest_accepted_id = accepted_id
                    value_to_propose = accepted_val

        # If we didn't get a strict mathematical majority, Phase 1 fails.
        if promises_received < majority:
            return (False, None)

        # ==========================================
        # PHASE 2: ACCEPT
        # ==========================================
        accepts_received = 0

        for acceptor in self.acceptors:
            # Simulate network packet loss
            if random.random() < simulate_network_drop:
                continue

            if acceptor.receive_accept(proposal_id, value_to_propose):
                accepts_received += 1

        # If a majority accepted the final value, consensus is achieved.
        if accepts_received >= majority:
            return (True, value_to_propose)

        return (False, None)