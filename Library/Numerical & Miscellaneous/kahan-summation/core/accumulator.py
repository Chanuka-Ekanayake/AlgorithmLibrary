"""
Kahan Summation Algorithm implementation.

This module provides an implementation of the Kahan summation algorithm,
also known as compensated summation. It mathematically reduces the numerical
error obtained when adding a sequence of finite-precision floating-point
numbers, compared to the standard approach.

In standard summation, adding a large number of values can result in
accumulated round-off errors because precision is lost when a small
number is added to a large number. Kahan summation achieves higher
precision by keeping a separate running compensation (a variable to
accumulate small errors that would otherwise be discarded).

Reference:
- Kahan, William (1965), "Further remarks on reducing truncation errors",
  Communications of the ACM, 8 (1): 40.

Typical usage:
    from kahan_summation.core.accumulator import kahan_sum, KahanAccumulator
    
    # 1. Functional approach:
    numbers = [0.1] * 10
    total = kahan_sum(numbers)
    print(total)  # 1.0 (standard sum might return something like 0.9999999999999999)
    
    # 2. Stateful / Accumulator approach:
    acc = KahanAccumulator()
    for n in numbers:
        acc.add(n)
    print(acc.get_sum())  # 1.0
"""

from typing import Iterable, Union, List, Iterator

class KahanAccumulator:
    """
    A stateful accumulator for performing Kahan summation iteratively.
    
    This class is highly useful when you have a stream of numbers coming in
    one by one and you want to maintain the compensated sum iteratively
    without storing all the numbers in memory at once. It reduces round-off
    error compared to a naive running total.
    
    Attributes:
        sum_ (float): The current running total.
        c (float): A running compensation for lost low-order bits.
    """
    
    def __init__(self, initial_value: float = 0.0) -> None:
        """
        Initializes the Kahan Accumulator.
        
        Args:
            initial_value (float): The starting value of the summation.
        """
        self.sum_: float = initial_value
        self.c: float = 0.0

    def add(self, value: Union[float, int]) -> None:
        """
        Adds a single value to the running total using Kahan's logic.
        
        Args:
            value (Union[float, int]): The number to add to the sum.
        """
        # y represents the element to add, minus the compensation
        # from the previous operation.
        y: float = float(value) - self.c
        
        # t represents the new sum. However, if sum_ is large and y is small, 
        # the low-order digits of y are lost.
        t: float = self.sum_ + y
        
        # (t - sum_) recovers the high-order part of y. 
        # Subtracting y recovers the lost low-order part as negative.
        self.c = (t - self.sum_) - y
        
        # Finally, we assign the new sum.
        self.sum_ = t

    def add_iterable(self, values: Iterable[Union[float, int]]) -> None:
        """
        Adds multiple values from an iterable to the running total.
        
        Args:
            values (Iterable[Union[float, int]]): A collection of numbers to add.
        """
        for value in values:
            self.add(value)

    def get_sum(self) -> float:
        """
        Retrieves the final compensated sum.
        
        Returns:
            float: The current accumulated sum.
        """
        return self.sum_
        
    def reset(self, new_initial_value: float = 0.0) -> None:
        """
        Resets the accumulator state.
        
        Args:
            new_initial_value (float): The starting value after reset.
        """
        self.sum_ = new_initial_value
        self.c = 0.0

def kahan_sum(values: Iterable[Union[float, int]]) -> float:
    """
    Computes the sum of a sequence of numbers using Kahan summation.
    
    This functional implementation is typically used when all values are
    readily available in an iterable (e.g., a list, tuple, or generator).
    
    Args:
        values (Iterable[Union[float, int]]): The sequence of numbers.
        
    Returns:
        float: The exact compensated sum of the values.
        
    Raises:
        TypeError: If the input is not iterable.
        
    Examples:
        >>> kahan_sum([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
        1.0
        
        >>> kahan_sum((1e10, 1.0, -1e10, 1.0))
        2.0
    """
    total: float = 0.0
    compensation: float = 0.0
    
    for val in values:
        y: float = float(val) - compensation
        t: float = total + y
        compensation = (t - total) - y
        total = t
        
    return total

def naive_sum(values: Iterable[Union[float, int]]) -> float:
    """
    Computes the naive sum for demonstration and benchmarking purposes.
    
    This is what standard built-in summations generally execute (though
    languages like Python have `math.fsum` for exact summation).
    
    Args:
        values (Iterable[Union[float, int]]): The sequence of numbers.
        
    Returns:
        float: The sum computed sequentially with standard precision loss.
    """
    total: float = 0.0
    for val in values:
        total += float(val)
    return total
