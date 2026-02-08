"""
Raft Consensus - Leader Election Module
Implements the core state machine for distributed consensus nodes.
Handles election timeouts, term management, and vote transitions.
"""

import time
import random
from enum import Enum
from typing import List

class State(Enum):
    FOLLOWER = 1
    CANDIDATE = 2
    LEADER = 3

class RaftNode:
    """
    A single node in a Raft cluster.
    Focuses on the Leader Election safety and state transitions.
    """

    def __init__(self, node_id: int, peer_ids: List[int]):
        self.node_id = node_id
        self.peer_ids = peer_ids
        
        # Persistent state
        self.current_term = 0
        self.voted_for = None
        
        # Volatile state
        self.state = State.FOLLOWER
        self.votes_received = set()
        
        # Election settings (Randomized to prevent split votes)
        self.election_timeout = random.uniform(0.150, 0.300) # 150-300ms
        self.last_heartbeat = time.time()

    def tick(self):
        """
        The main internal loop for a node.
        Checks for election timeouts and handles state-specific behavior.
        """
        if self.state == State.LEADER:
            self._send_heartbeats()
        else:
            # If we haven't heard from the leader within the timeout...
            if time.time() - self.last_heartbeat > self.election_timeout:
                self._start_election()

    def _start_election(self):
        """
        Transitions to CANDIDATE state and requests votes from peers.
        """
        self.state = State.CANDIDATE
        self.current_term += 1
        self.voted_for = self.node_id
        self.votes_received = {self.node_id}
        self.last_heartbeat = time.time() # Reset timer for this term
        
        print(f"[NODE {self.node_id}] Timeout! Starting election for Term {self.current_term}")

    def handle_request_vote(self, term: int, candidate_id: int) -> bool:
        """
        Decides whether to grant a vote to a candidate.
        Safety Rule: Can only vote for one candidate per term.
        """
        # If candidate's term is older, reject
        if term < self.current_term:
            return False
            
        # If we see a newer term, revert to follower
        if term > self.current_term:
            self.current_term = term
            self.state = State.FOLLOWER
            self.voted_for = None

        # If we haven't voted yet (or already voted for this candidate), grant vote
        if self.voted_for is None or self.voted_for == candidate_id:
            self.voted_for = candidate_id
            self.last_heartbeat = time.time() # Reset timeout as we recognize a valid candidate
            return True
            
        return False

    def handle_vote_response(self, term: int, granted: bool, peer_id: int):
        """
        Processes a vote from a peer. 
        If a majority is reached, transitions to LEADER.
        """
        if self.state != State.CANDIDATE or term != self.current_term:
            return

        if granted:
            self.votes_received.add(peer_id)
            
            # Quorum check: (N / 2) + 1
            quorum = (len(self.peer_ids) + 1) // 2 + 1
            if len(self.votes_received) >= quorum:
                self._become_leader()

    def _become_leader(self):
        """Transition to LEADER state and begin heartbeat cycle."""
        self.state = State.LEADER
        print(f"👑 [NODE {self.node_id}] Elected LEADER for Term {self.current_term}!")

    def _send_heartbeats(self):
        """Simulates sending heartbeats to keep followers suppressed."""
        # In a real system, this triggers AppendEntries RPCs
        self.last_heartbeat = time.time()

    def handle_heartbeat(self, term: int, leader_id: int):
        """Follower logic: Recognize a valid leader and reset election timer."""
        if term >= self.current_term:
            self.current_term = term
            self.state = State.FOLLOWER
            self.last_heartbeat = time.time()