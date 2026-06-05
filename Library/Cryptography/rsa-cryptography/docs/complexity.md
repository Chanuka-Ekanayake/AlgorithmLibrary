# Complexity Analysis of RSA

The complexity of the RSA algorithm depends heavily on the size of the keys used (i.e., the bit length of the modulus $n$, denoted as $k$). Let $k$ be the number of bits in $n$.

## 1. Key Generation
*   **Prime Generation:** Generating a $k$-bit prime involves picking random numbers and applying a primality test. By the Prime Number Theorem, a random $k$-bit integer is prime with probability $\approx 1/\ln(2^k) \approx 1/(0.69 \cdot k)$. Thus, we expect to test $O(k)$ candidates.
*   **Miller-Rabin Primality Test:** The Miller-Rabin test takes $O(k^3)$ time per candidate. Since we test $O(k)$ candidates, generating a single prime takes expected time $O(k^4)$. With fast multiplication algorithms, this can be reduced to $O(k^3)$ or $O(k^4 / \log k)$.
*   **Extended Euclidean Algorithm:** Computing the inverse $d \equiv e^{-1} \pmod{\phi(n)}$ using the Extended Euclidean Algorithm takes $O(k^2)$ time.
*   **Overall Key Generation:** Dominated by prime generation, the overall time complexity is $O(k^4)$ per key pair.

## 2. Encryption
Encryption computes $c \equiv M^e \pmod n$.
*   Using modular exponentiation (square and multiply), this requires $O(\log e)$ multiplications.
*   Since $e$ is generally chosen to be small (like $65537 = 2^{16} + 1$), the number of operations is a small constant (e.g., 17 multiplications).
*   Each modular multiplication of $k$-bit numbers takes $O(k^2)$ time.
*   **Overall Encryption:** $O(k^2 \log e)$. For small constant $e$, this is $O(k^2)$.

## 3. Decryption
Decryption computes $M \equiv c^d \pmod n$.
*   Using modular exponentiation, this requires $O(\log d)$ multiplications.
*   Since $d$ can be as large as $\phi(n)$, it has about $k$ bits. Thus, $O(k)$ multiplications are needed.
*   Each modular multiplication of $k$-bit numbers takes $O(k^2)$ time.
*   **Overall Decryption:** $O(k^3)$. Decryption is significantly slower than encryption when $e$ is chosen to be small.

## Summary
*   **Key Generation:** $O(k^4)$ Expected Time
*   **Encryption:** $O(k^2 \log e)$ Time
*   **Decryption:** $O(k^3)$ Time
