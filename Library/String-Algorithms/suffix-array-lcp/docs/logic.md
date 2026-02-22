# Algorithm Logic: Suffix Array + LCP Array

## 1. The Problem with Naive Substring Search

Imagine you are running a plagiarism-detection service. A document arrives, and you must simultaneously check it against thousands of previously stored documents. A naive approach — comparing the input against every stored string character-by-character — is catastrophically slow on large corpora.

The Suffix Array is the data structure that makes this tractable. It can be built once per document and then answer **any** substring query in **O(M log N)** time, where M is the length of the query pattern.

---

## 2. What Is a Suffix?

A **suffix** of a string `S` of length `N` is any substring that starts at position `i` and runs to the end of `S`.

For the string `"banana"`, the suffixes are:

| Start Index | Suffix       |
| ----------- | ------------ |
| 0           | `"banana"`   |
| 1           | `"anana"`    |
| 2           | `"nana"`     |
| 3           | `"ana"`      |
| 4           | `"na"`       |
| 5           | `"a"`        |

A **Suffix Array** is simply the list of these starting indices, sorted by the lexicographic (alphabetical) order of the suffixes they represent.

**Sorted order for `"banana"`:**

| SA Rank | Start Index | Suffix       |
| ------- | ----------- | ------------ |
| 0       | 5           | `"a"`        |
| 1       | 3           | `"ana"`      |
| 2       | 1           | `"anana"`    |
| 3       | 0           | `"banana"`   |
| 4       | 4           | `"na"`       |
| 5       | 2           | `"nana"`     |

**Resulting SA:** `[5, 3, 1, 0, 4, 2]`

---

## 3. Building the Suffix Array: Prefix-Doubling (O(N log N))

Naively sorting all N suffixes costs O(N² log N) because comparing two suffixes can take O(N) time. Prefix-Doubling (Manber & Myers, 1990) reduces this to O(N log N).

### The Core Idea

Assign each suffix a **rank** based on its first `2^k` characters. In each round, double `k`:

- **Round 0 (k=0):** Rank by the first `1` character (character ordinal).
- **Round 1 (k=1):** Rank by pairs of Round 0 ranks →  first `2` characters.
- **Round 2 (k=2):** Rank by pairs of Round 1 ranks → first `4` characters.
- **…continue until all ranks are unique.**

### Walkthrough for `"aab"`

Append sentinel `'$'` → `"aab$"`.

**Round 0:** Sort by character.

| Suffix | Rank |
| ------ | ---- |
| `$`    | 0    |
| `a`    | 1    |
| `ab$`  | 1    |
| `aab$` | 1    |
| `b$`   | 2    |

**Round 1:** Sort by (rank[i], rank[i+1]) pairs. Ties are now broken.

After each round, ranks are re-assigned as consecutive integers, preserving relative order. After `ceil(log₂ N)` rounds, all ranks are unique and the Suffix Array is complete.

---

## 4. The LCP Array: Kasai's Algorithm (O(N))

The **Longest Common Prefix (LCP)** array stores how many characters consecutive entries in the Suffix Array share.

`lcp[i]` = length of the longest common prefix of the suffixes starting at `sa[i-1]` and `sa[i]`.

### Key Lemma (Kasai, 2001)

> If suffix at position `p` has `lcp[rank[p]] = h`, then the suffix at position `p+1` has `lcp[rank[p+1]] >= h - 1`.

**Why?** Because removing the first character from a suffix can reduce its LCP with its predecessor by at most 1. This means we can process suffixes in text order and **carry the LCP count forward**, performing only O(N) character comparisons total.

### Walkthrough for `SA = [5, 3, 1, 0, 4, 2]` (`"banana$"`)

| i | SA[i] | Suffix        | LCP with previous |
| - | ----- | ------------- | ----------------- |
| 0 | 6     | `$`           | 0 (by definition) |
| 1 | 5     | `a$`          | 0                 |
| 2 | 3     | `ana$`        | 1 (`"a"`)         |
| 3 | 1     | `anana$`      | 3 (`"ana"`)       |
| 4 | 0     | `banana$`     | 0                 |
| 5 | 4     | `na$`         | 0                 |
| 6 | 2     | `nana$`       | 2 (`"na"`)        |

---

## 5. Substring Search Using the Suffix Array (O(M log N))

Because all suffixes are sorted, any query pattern `P` of length `M` must appear as a **prefix** of a contiguous block of entries in the Suffix Array. We find this block with two binary searches:

1. **Left boundary:** first index where `sa[i]` has `P` as a prefix.
2. **Right boundary:** first index where the prefix no longer matches.

All indices in `[left, right)` are match positions.

---

## 6. System Relevance

When a genome-sequencing pipeline must find all locations of a short DNA probe inside a 3-billion-base chromosome, building a Suffix Array once and issuing thousands of O(M log N) queries is the only feasible approach — a brute-force O(N·M) search per query would take hours.
