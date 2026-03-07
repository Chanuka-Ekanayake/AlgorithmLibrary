import sys
import os

# Add the parent directory to the Python path to import from core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.decoder import ViterbiDecoder

def run_weather_example():
    """
    Scenario 1:
    You are locked in a room. You can only observe what your friend is wearing 
    or doing when they come to visit to deduce the weather outside.
    States: "Rainy", "Sunny"
    Observations: "walk", "shop", "clean"
    """
    print("\n" + "="*60)
    print("SCENARIO 1: WEATHER DEDUCTION HMM")
    print("="*60)
    
    states = ["Rainy", "Sunny"]
    observations = ["walk", "shop", "clean"]
    
    start_prob = {
        "Rainy": 0.6,
        "Sunny": 0.4
    }
    
    trans_prob = {
        "Rainy": {"Rainy": 0.7, "Sunny": 0.3},
        "Sunny": {"Rainy": 0.4, "Sunny": 0.6},
    }
    
    emit_prob = {
        "Rainy": {"walk": 0.1, "shop": 0.4, "clean": 0.5},
        "Sunny": {"walk": 0.6, "shop": 0.3, "clean": 0.1},
    }
    
    decoder = ViterbiDecoder(states, observations, start_prob, trans_prob, emit_prob)
    
    # Let's say we observe our friend over 3 days:
    sequence = ["walk", "shop", "clean"]
    
    print(f"Observation Sequence: {sequence}")
    
    best_path, path_prob = decoder.decode(sequence)
    
    print(f"Most likely weather sequence: {best_path}")
    print(f"Calculated Sequence Probability: {path_prob:.8f}")
    
    # Expected output derived from hand-calculation:
    # 1. Start: Sunny(0.4*0.6=0.24) > Rainy(0.6*0.1=0.06) -> Day 1 = Sunny
    # 2. Trans to Day 2 (shop): 
    #    Sunny->Sunny(0.24*0.6*0.3=0.0432)
    #    Sunny->Rainy(0.24*0.4*0.4=0.0384) -> Day 2 = Rainy (due to shop multiplier)
    print("-" * 60)


def run_pos_tagging_example():
    """
    Scenario 2:
    Part-of-Speech tagging. We have a tiny vocabulary and want to predict 
    if a word acts as a Noun or a Verb based on its context within a sentence.
    States: "Noun", "Verb", "Adj"
    Observations: "bear", "is", "funny", "they", "hunt"
    """
    print("\n" + "="*60)
    print("SCENARIO 2: PART OF SPEECH TAGGING HMM")
    print("="*60)
    
    states = ["Noun", "Verb", "Adj"]
    observations = ["bear", "is", "funny", "they", "hunt"]
    
    # Assuming the sentence is starting...
    start_prob = {
        "Noun": 0.7,
        "Verb": 0.1,
        "Adj": 0.2
    }
    
    # Transition: Noun usually followed by Verb. Verb usually followed by Noun/Adj.
    trans_prob = {
        "Noun": {"Noun": 0.1, "Verb": 0.7, "Adj": 0.2},
        "Verb": {"Noun": 0.5, "Verb": 0.1, "Adj": 0.4},
        "Adj":  {"Noun": 0.9, "Verb": 0.05, "Adj": 0.05}
    }
    
    emit_prob = {
        # "bear" can be Noun (animal) or Verb (to carry)
        "Noun": {"bear": 0.4, "is": 0.0, "funny": 0.0, "they": 0.5, "hunt": 0.1},
        "Verb": {"bear": 0.3, "is": 0.4, "funny": 0.0, "they": 0.0, "hunt": 0.3},
        "Adj":  {"bear": 0.0, "is": 0.0, "funny": 1.0, "they": 0.0, "hunt": 0.0}     
    }
    
    decoder = ViterbiDecoder(states, observations, start_prob, trans_prob, emit_prob)
    
    sentences = [
        ["they", "hunt", "bear"],          # expected: Noun, Verb, Noun
        ["bear", "is", "funny"],           # expected: Noun, Verb, Adj
    ]
    
    for words in sentences:
        print(f"Observation Sequence: {words}")
        best_path, path_prob = decoder.decode(words)
        print(f"Predicted POS Tags:   {best_path}")
        print(f"Calculated Sequence Probability: {path_prob:.8f}\n")
    print("-" * 60)


def main():
    print("Initializing Viterbi Decoder Test Suite...")
    
    try:
        run_weather_example()
        run_pos_tagging_example()
    except Exception as e:
        print(f"An error occurred during decoding: {e}")
        sys.exit(1)
        
    print("\nAll tests executed successfully.")

if __name__ == "__main__":
    main()
