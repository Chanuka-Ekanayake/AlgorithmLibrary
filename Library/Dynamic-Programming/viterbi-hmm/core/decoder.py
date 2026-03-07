from typing import List, Tuple, Dict, Any

class ViterbiDecoder:
    """
    Implements the Viterbi Decoder for Hidden Markov Models (HMM).
    
    This class takes the standard components of an HMM:
    - States: The hidden states.
    - Observations: The possible emissions/observations.
    - Start Probabilities: Probability distribution of the initial state.
    - Transition Matrix: Probabilities of transitioning between states.
    - Emission Matrix: Probabilities of observations given states.

    It provides methods to decode the most likely sequence of hidden states
    given a sequence of observations.
    """

    def __init__(
        self, 
        states: List[str], 
        observations: List[str], 
        start_prob: Dict[str, float], 
        transition_prob: Dict[str, Dict[str, float]], 
        emission_prob: Dict[str, Dict[str, float]]
    ):
        """
        Initializes the ViterbiDecoder with the HMM parameters.

        Args:
            states: A list of string labels for the hidden states.
            observations: A list of string labels for the possible observations.
            start_prob: A dictionary mapping state -> initial probability.
            transition_prob: A nested dictionary mapping state1 -> state2 -> probability.
            emission_prob: A nested dictionary mapping state -> observation -> probability.
        """
        self.states = states
        self.observations = observations
        self.start_prob = start_prob
        self.transition_prob = transition_prob
        self.emission_prob = emission_prob
        
        self._validate_model()

    def _validate_model(self) -> None:
        """
        Validates the HMM matrices to ensure probabilities sum up to 1.0 
        (within a small floating-point tolerance).
        
        Raises:
            ValueError: If probabilities are significantly off.
        """
        tolerance = 1e-5
        
        # Check start probabilities
        total_start = sum(self.start_prob.values())
        if abs(total_start - 1.0) > tolerance:
            raise ValueError(f"Start probabilities must sum to 1.0, got {total_start}")
            
        # Check transition probabilities
        for state in self.states:
            if state not in self.transition_prob:
                raise ValueError(f"State '{state}' missing from transition matrix.")
            
            trans_sum = sum(self.transition_prob[state].values())
            if abs(trans_sum - 1.0) > tolerance:
                raise ValueError(
                    f"Transition probabilities from state '{state}' must sum to 1.0, got {trans_sum}"
                )
                
        # Check emission probabilities
        for state in self.states:
            if state not in self.emission_prob:
                raise ValueError(f"State '{state}' missing from emission matrix.")
                
            emit_sum = sum(self.emission_prob[state].values())
            if abs(emit_sum - 1.0) > tolerance:
                raise ValueError(
                    f"Emission probabilities from state '{state}' must sum to 1.0, got {emit_sum}"
                )

    def decode(self, observation_sequence: List[str]) -> Tuple[List[str], float]:
        """
        Decodes the most likely sequence of hidden states given an observation sequence.

        This uses the core Viterbi dynamic programming algorithm. 
        It maintains two tables (DP matrices):
        1. V[state][time]: the maximum probability of the sequence up to `time` ending in `state`.
        2. backpointer[state][time]: the state at `time-1` that maximized V[state][time].

        Args:
            observation_sequence: A list of observations to decode.

        Returns:
            A tuple containing:
            - The most likely sequence of hidden states (List[str]).
            - The probability of this sequence (float).
            
        Raises:
            ValueError: If an unknown observation is encountered or sequence is empty.
        """
        if not observation_sequence:
            return [], 0.0

        for obs in observation_sequence:
            if obs not in self.observations:
                raise ValueError(f"Unknown observation encountered: '{obs}'")

        T = len(observation_sequence)
        
        # Initialize Viterbi table (V) and backpointer table
        # V keeps track of the maximum probability
        # Backpointer keeps track of the best previous state
        V: List[Dict[str, float]] = [{} for _ in range(T)]
        backpointer: List[Dict[str, str]] = [{} for _ in range(T)]

        # ---------------------------------------------------------------------
        # Initialization Step (t=0)
        # ---------------------------------------------------------------------
        first_obs = observation_sequence[0]
        for state in self.states:
            # Probability = initial probability * emission probability of first obs
            V[0][state] = self.start_prob[state] * self.emission_prob[state][first_obs]
            backpointer[0][state] = None  # No previous state at t=0

        # ---------------------------------------------------------------------
        # Recursion Step (t=1 to T-1)
        # ---------------------------------------------------------------------
        for t in range(1, T):
            obs = observation_sequence[t]
            
            for current_state in self.states:
                max_prob = -1.0
                best_prev_state = None
                
                # We need to find the specific previous state that gives us 
                # the highest probability to arrive at the current state.
                for prev_state in self.states:
                    
                    # Previous Viterbi probability
                    prev_v_prob = V[t - 1][prev_state]
                    
                    # Transition probability from prev_state -> current_state
                    trans_prob = self.transition_prob[prev_state][current_state]
                    
                    # Emission probability of getting `obs` while in `current_state`
                    emit_prob = self.emission_prob[current_state][obs]
                    
                    # Total probability for this path
                    prob = prev_v_prob * trans_prob * emit_prob
                    
                    if prob > max_prob:
                        max_prob = prob
                        best_prev_state = prev_state
                
                # Store the maximum probability and the backpointer
                V[t][current_state] = max_prob
                backpointer[t][current_state] = best_prev_state

        # ---------------------------------------------------------------------
        # Termination Step
        # ---------------------------------------------------------------------
        # Find the state that has the maximum probability at the final time step T-1
        best_final_state = max(self.states, key=lambda st: V[T - 1][st])
        max_path_probability = V[T - 1][best_final_state]

        # ---------------------------------------------------------------------
        # Backtracking Step (Path Reconstruction)
        # ---------------------------------------------------------------------
        # We start from the best final state and use the backpointers to trace 
        # the path backward to the beginning.
        best_path = [best_final_state]
        curr_state = best_final_state
        
        # Go backwards from T-1 down to 1
        for t in range(T - 1, 0, -1):
            prev_state_for_curr = backpointer[t][curr_state]
            best_path.insert(0, prev_state_for_curr)
            curr_state = prev_state_for_curr

        return best_path, max_path_probability
