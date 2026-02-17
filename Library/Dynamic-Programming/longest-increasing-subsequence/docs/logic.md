# Algorithm Logic: Longest Increasing Subsequence (LIS)

The goal of the LIS algorithm is to find the longest sequence of elements in an array that are in strictly increasing order. They do not need to be contiguous (next to each other) in the original array.

## 1. The Classic DP Approach (The Baseline)

The approach solves the problem by breaking it into smaller subproblems.
We maintain an array , where represents the length of the longest increasing subsequence that strictly ends at the element .

For every element , we look back at every previous element . If , we can append to the subsequence ending at .
Mathematically:

While easy to implement, looking back at _every_ previous element causes the bottleneck.

---

## 2. The Breakthrough: Patience Sorting

To optimize the search, we use a technique modeled after the card game "Patience" (Solitaire).

Imagine iterating through your array and treating each number as a card drawn from a deck. You are placing these cards into piles from left to right based on the following rules:

1. A card must be placed on a pile where the top card is **larger** than the current card.
2. If multiple piles are valid, place the card on the **leftmost** valid pile.
3. If no pile has a top card larger than the current card, start a **new pile** to the right.

**The Golden Rule:** The number of piles at the end of the game equals the length of the Longest Increasing Subsequence.

---

## 3. Translating Cards to Code (The `tails` Array)

In our code, the `tails` array represents the "top card" of each pile.

Because of how the game is played, the values in the `tails` array are **always strictly increasing**.

- Why? Because we only start a new pile to the right if a card is larger than _all_ existing top cards.

Because the `tails` array is always sorted, we don't need to scan it linearly. We can use **Binary Search** to instantly find the correct pile for the next card, reducing the lookup time from to .

---

## 4. The Reconstruction Challenge

Returning the _length_ of the LIS (the number of piles) is easy. Returning the _actual sequence_ is much harder.

When a card is placed on a pile, it doesn't just form a sequence with the cards below it in the _same_ pile. It forms a sequence with a card in the pile immediately to its **left**.

To reconstruct the path:

1. Every time we place a card, we record a pointer (in a `parent` array) to the top card of the pile immediately to its left.
2. Once all cards are dealt, we start at the top card of the rightmost pile and follow the pointers backwards to rebuild the sequence.
