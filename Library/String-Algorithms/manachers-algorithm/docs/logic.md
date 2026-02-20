# Algorithm Logic: Manacher’s Algorithm

The core challenge of finding palindromes is dealing with their centers.
Odd-length palindromes (like `"aba"`) have a single character center (`'b'`). Even-length palindromes (like `"abba"`) have an "invisible" center between the two `'b'`s.

Manacher’s Algorithm solves this, and the efficiency problem, in two distinct phases.

## 1. Phase 1: The Preprocessing Trick

To eliminate the even/odd center problem, we transform the string by injecting a dummy character (usually `#`) between every letter, and special sentinels (`^` and `$`) at the ends.

- **Odd Example:** `"aba"` becomes `"^#a#b#a#$"` (Length 9)
- **Even Example:** `"abba"` becomes `"^#a#b#b#a#$"` (Length 11)

Now, _every_ palindrome has a distinct, physical center (either a letter or a `#`). The sentinels `^` and `$` guarantee that when we expand our search outwards, we will hit a boundary character before throwing an `IndexError`, saving us from writing expensive `if/else` edge checks in our loop.

---

## 2. Phase 2: The Core Variables

As we scan through the transformed string from left to right, we maintain a few critical pieces of information:

- **`P` Array:** An array where `P[i]` stores the _radius_ of the longest palindrome centered at index `i`.
- **`C` (Center):** The center index of the palindrome that currently extends furthest to the right.
- **`R` (Right Boundary):** The rightmost index that the palindrome centered at `C` reaches. (`R = C + P[C]`).
- **`i`:** Our current index as we iterate through the string.

---

## 3. The Magic of Mirroring

The true genius of Manacher’s Algorithm lies in how it uses the `C` and `R` variables to look backward in time.

Because a palindrome is symmetrical, the left side of `C` is a perfect mirror image of the right side of `C`. Therefore, if we are at an index `i` (which is to the right of `C`), we can look at its "mirror" index on the left side of `C`.

**The Mirror Formula:** `mirror = 2 * C - i`

### The Three Scenarios

When we look at `P[mirror]`, one of three things is true:

1. **Fully Contained:** The palindrome at `mirror` is short and fits entirely inside our known boundary `R`.

- _Action:_ Because of symmetry, the palindrome at `i` must be exactly the same length. `P[i] = P[mirror]`. No expansion needed!

2. **Extends Past Boundary:** The palindrome at `mirror` is huge and extends past the left boundary of `C`.

- _Action:_ We only know for a _fact_ that the string is symmetrical up to `R`. Therefore, the palindrome at `i` is _at least_ `R - i` long. `P[i] = R - i`. We must then manually expand to see if it goes further.

3. **Exactly on the Boundary:** The palindrome at `mirror` perfectly touches the left boundary of `C`.

- _Action:_ The palindrome at `i` is at least `P[mirror]` long, but it might be longer since we haven't explored past `R` yet. We set `P[i] = P[mirror]` and manually expand.

The code elegantly handles all three scenarios with a single line:

```python
if i < R:
    P[i] = min(R - i, P[mirror])

```

By safely copying the radius from the left side, the algorithm skips thousands of redundant character comparisons, resulting in strict performance.
