# Algorithm Logic: Knuth-Morris-Pratt (KMP)

## 1. The Backtracking Problem

In a brute-force search, if you are looking for the word `"TRANSFORMER"` and you match `"TRANSFORM"`, but the next character is an `"X"` instead of an `"E"`, the algorithm throws away all that work. It moves the text pointer back to the `"R"` (the second letter of the text) and starts over.

KMP recognizes that this is highly inefficient. If you already know you matched `"TRANSFORM"`, you know exactly what characters are currently behind your text pointer. You shouldn't need to read them again.

---

## 2. The LPS Array (The Pi Table)

The core of KMP is the **Longest Proper Prefix which is also Suffix (LPS)** array. Before searching the text, KMP analyzes the search pattern itself.

- **Proper Prefix:** Any leading substring of a string, excluding the string itself. (For `"ABC"`, prefixes are `"A"`, `"AB"`).
- **Suffix:** Any trailing substring of a string. (For `"ABC"`, suffixes are `"C"`, `"BC"`, `"ABC"`).

The LPS array stores the length of the longest prefix that matches a suffix for every sub-pattern.

---

## 3. Building the LPS Array: A Walkthrough

Let's build the LPS array for the pattern: **`"ABABCABAB"`**

| Index | Character | Sub-pattern   | Longest Prefix that is also Suffix | LPS Value |
| ----- | --------- | ------------- | ---------------------------------- | --------- |
| 0     | A         | `"A"`         | None                               | **0**     |
| 1     | B         | `"AB"`        | None                               | **0**     |
| 2     | A         | `"ABA"`       | `"A"`                              | **1**     |
| 3     | B         | `"ABAB"`      | `"AB"`                             | **2**     |
| 4     | C         | `"ABABC"`     | None (The 'C' breaks the pattern)  | **0**     |
| 5     | A         | `"ABABCA"`    | `"A"`                              | **1**     |
| 6     | B         | `"ABABCAB"`   | `"AB"`                             | **2**     |
| 7     | A         | `"ABABCABA"`  | `"ABA"`                            | **3**     |
| 8     | B         | `"ABABCABAB"` | `"ABAB"`                           | **4**     |

**Resulting LPS Array:** `[0, 0, 1, 2, 0, 1, 2, 3, 4]`

---

## 4. The Search Execution

Once the LPS array is built, the search begins using two pointers: for the Text, and for the Pattern.

1. **Match:** If `Text[i] == Pattern[j]`, increment both and .
2. **Mismatch:** If `Text[i] != Pattern[j]`:

- We know the characters before successfully matched.
- We look at `LPS[j - 1]`. This number tells us the length of the prefix that we _already know_ exists right before our current position.
- We shift our pattern pointer to `j = LPS[j - 1]`.
- **Crucially, the text pointer never moves backward.**

By shifting instead of , we align the known prefix of our pattern with the matching suffix we just found in the text, allowing the search to continue seamlessly.

---

## 5. System Relevance

When a user on your platform searches for a specific string like `"image-verification-api"` inside a massive, 10,000-word documentation file, KMP guarantees the server only reads those 10,000 words exactly once. It completely eliminates the CPU spikes caused by worst-case backtracking scenarios.
