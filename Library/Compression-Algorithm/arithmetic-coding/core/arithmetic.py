"""
Arithmetic Coding Compression
An entropy encoding algorithm that maps an entire sequence of symbols 
to a single fractional number in the interval [0.0, 1.0).
"""

from decimal import Decimal, getcontext
from typing import Dict, Tuple

class ArithmeticCoder:
    """
    Encodes and decodes messages using continuous interval subdivision.
    """

    def __init__(self, text: str, precision: int = 150):
        """
        Initializes the coder, calculates symbol probabilities, and sets precision.
        
        Args:
            text: The sample text to build the frequency table from.
            precision: The number of decimal places to track (prevents underflow).
        """
        getcontext().prec = precision
        self.probability_table = self._build_probability_table(text)

    def _build_probability_table(self, text: str) -> Dict[str, Tuple[Decimal, Decimal]]:
        """
        Calculates the cumulative probability range [low, high) for each symbol.
        """
        if not text:
            raise ValueError("Input text cannot be empty.")

        # 1. Calculate raw frequencies
        frequencies = {}
        for char in text:
            frequencies[char] = frequencies.get(char, 0) + 1

        # 2. Convert to cumulative probabilities
        total_chars = Decimal(len(text))
        probability_table = {}
        current_low = Decimal(0.0)

        # Sort keys to ensure deterministic table generation
        for char in sorted(frequencies.keys()):
            probability = Decimal(frequencies[char]) / total_chars
            current_high = current_low + probability
            
            # Store the [low, high) bounds for this character
            probability_table[char] = (current_low, current_high)
            current_low = current_high

        return probability_table

    def encode(self, message: str) -> Decimal:
        """
        Encodes a string message into a single Decimal number.
        """
        low = Decimal(0.0)
        high = Decimal(1.0)

        for char in message:
            if char not in self.probability_table:
                raise ValueError(f"Character '{char}' not in probability table.")

            # Calculate the current interval range
            current_range = high - low
            
            # Fetch the bounds for the specific character
            char_low, char_high = self.probability_table[char]

            # Narrow the interval
            high = low + (current_range * char_high)
            low = low + (current_range * char_low)

        # Any number within the final [low, high) interval represents the message.
        # Returning 'low' is standard practice.
        return low

    def decode(self, encoded_value: Decimal, message_length: int) -> str:
        """
        Decodes a Decimal number back into the original string.
        Requires the original message length to know when to stop decoding.
        """
        # Validate that the encoded value lies within the expected interval.
        if not (Decimal(0) <= encoded_value < Decimal(1)):
            raise ValueError("encoded_value must be within the interval [0, 1).")

        decoded_message = []
        current_value = encoded_value

        for position in range(message_length):
            symbol_found = False
            # 1. Find which character's interval contains the current_value
            for char, (char_low, char_high) in self.probability_table.items():
                if char_low <= current_value < char_high:
                    decoded_message.append(char)

                    # 2. "Zoom in" on this interval for the next iteration
                    # V_new = (V_old - low) / (high - low)
                    current_range = char_high - char_low
                    current_value = (current_value - char_low) / current_range
                    symbol_found = True
                    break

            if not symbol_found:
                raise ValueError(
                    f"Encoded value does not correspond to a valid symbol "
                    f"at position {position}."
                )
        return "".join(decoded_message)