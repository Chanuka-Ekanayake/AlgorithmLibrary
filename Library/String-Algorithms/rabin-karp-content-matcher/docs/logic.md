# Algorithm Logic: Rabin-Karp Rolling Hash

## 1. The Core Concept

The Rabin-Karp algorithm is designed to solve the **String Matching** problem. While a naive search checks every character of a pattern against every character of a text, Rabin-Karp uses **Hashing** to filter out mismatches instantly.

The "Magic" of this algorithm is the **Rolling Hash**, which allows us to calculate the hash of a new window in  time based on the hash of the previous window.

---

## 2. The Polynomial Rolling Hash

To turn a string into a unique number (hash), we treat the string as a number in a specific base (usually the size of the alphabet, ).

### The Formula

For a string  of length :


* : Numerical value of the character (ASCII).
* : Base (number of characters in the alphabet).
* : A large prime number to prevent huge values and minimize collisions.

---

## 3. The "Rolling" Mechanism

When we slide the window one position to the right, we don't re-calculate the whole hash. We:

1. **Remove** the high-order digit (the character leaving the window).
2. **Shift** the remaining digits (multiply by the base ).
3. **Add** the new low-order digit (the character entering the window).

### The Rolling Update Formula:

* : The character leaving the window.
* : Pre-calculated value of .
* : The new character entering the window.

---

## 4. Handling Hash Collisions

Because we use a modulo (), different strings can occasionally produce the same hash. This is called a **Spurious Hit**.

* **The Guard:** When `p_hash == t_hash`, the algorithm performs a direct string comparison to ensure the match is real.
* **The Probability:** By using a very large prime (like ), the chance of a collision is extremely low, keeping the performance near .

---

## 5. Multiple Pattern Matching

One of Rabin-Karp's greatest strengths is its ability to search for **multiple patterns** at once. By pre-calculating the hashes of several different patterns, you can scan a document once and flag any of those patterns as you slide through the text.

---

## 6. Industrial Application: Plagiarism & Security

In your 2026 software marketplace, this logic is used for:

* **Malware Detection:** Scanning binary files for known "malicious byte signatures."
* **Plagiarism Checking:** Comparing student or developer code against a massive database of existing snippets.
* **Duplicate Content:** Ensuring that users aren't uploading the same software model multiple times under different names.