"""
Gale-Shapley Stable Matching Algorithm
Guarantees a stable bipartite matching between two equally sized sets of entities
based on their strict preference rankings.
"""

from collections import deque
from typing import Dict, List

class StableMatcher:
    """
    Combinatorial optimization engine for two-sided marketplaces.
    """

    @staticmethod
    def _validate_inputs(
        proposers: Dict[str, List[str]], 
        receivers: Dict[str, List[str]]
    ) -> None:
        """
        Ensures the market is perfectly balanced and preferences are valid.
        """
        if len(proposers) != len(receivers):
            raise ValueError("The number of Proposers and Receivers must be perfectly equal.")

        proposer_set = set(proposers.keys())
        receiver_set = set(receivers.keys())

        # Validate that every preference list contains exactly the members of the opposite set
        for p, prefs in proposers.items():
            if set(prefs) != receiver_set:
                raise ValueError(f"Proposer '{p}' does not have a valid ranking of all Receivers.")
                
        for r, prefs in receivers.items():
            if set(prefs) != proposer_set:
                raise ValueError(f"Receiver '{r}' does not have a valid ranking of all Proposers.")

    @classmethod
    def match(
        cls, 
        proposer_prefs: Dict[str, List[str]], 
        receiver_prefs: Dict[str, List[str]]
    ) -> Dict[str, str]:
        """
        Executes the Proposer-Optimal Stable Matching algorithm.
        
        Args:
            proposer_prefs: Dictionary mapping a Proposer to their ranked list of Receivers.
            receiver_prefs: Dictionary mapping a Receiver to their ranked list of Proposers.
            
        Returns:
            A dictionary mapping each Receiver to their finalized Proposer.
        """
        # 1. Edge-Case Validation
        cls._validate_inputs(proposer_prefs, receiver_prefs)

        # 2. State Tracking
        # Maps a Receiver to their currently matched Proposer
        matches: Dict[str, str] = {}
        
        # A queue of Proposers who currently do not have a match
        free_proposers = deque(proposer_prefs.keys())
        
        # Tracks how many proposals each Proposer has made (acts as an index for their preference list)
        proposal_counts: Dict[str, int] = {p: 0 for p in proposer_prefs}

        # 3. Time-Complexity Optimization (The Pre-Computation)
        # Convert receiver arrays: ['A', 'C', 'B'] into fast lookup dicts: {'A': 0, 'C': 1, 'B': 2}
        # This allows O(1) rank comparisons instead of O(N) array scans inside the while loop.
        receiver_ranks: Dict[str, Dict[str, int]] = {}
        for receiver, prefs in receiver_prefs.items():
            receiver_ranks[receiver] = {proposer: rank for rank, proposer in enumerate(prefs)}

        # 4. The Gale-Shapley Loop
        while free_proposers:
            # Get a free Proposer from the queue
            proposer = free_proposers.popleft()
            
            # Find the highest-ranked Receiver they haven't proposed to yet
            current_choice_index = proposal_counts[proposer]
            top_receiver = proposer_prefs[proposer][current_choice_index]
            
            # Record that this Proposer has officially asked this Receiver
            proposal_counts[proposer] += 1
            
            # Scenario A: The Receiver is completely unmatched. 
            # They must accept the proposal temporarily.
            if top_receiver not in matches:
                matches[top_receiver] = proposer
                
            # Scenario B: The Receiver is already matched. 
            # They will compare their current match against the new proposal.
            else:
                current_match = matches[top_receiver]
                
                # Lower rank value = better preference (Rank 0 is best)
                current_rank = receiver_ranks[top_receiver][current_match]
                new_rank = receiver_ranks[top_receiver][proposer]
                
                if new_rank < current_rank:
                    # The Receiver prefers the NEW Proposer. Break the old engagement.
                    matches[top_receiver] = proposer
                    # The old match is dumped back into the queue to try their next choice
                    free_proposers.append(current_match)
                else:
                    # The Receiver prefers their CURRENT match. Reject the new Proposer.
                    # The rejected Proposer goes back into the queue.
                    free_proposers.append(proposer)

        return matches