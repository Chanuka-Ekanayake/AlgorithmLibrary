from random import SystemRandom

rand = SystemRandom()
def gcd(a, b):
    """
    Euclid's algorithm for determining the greatest common divisor.
    """
    while b != 0:
        a, b = b, a % b
    return a

def multiplicative_inverse(e, phi):
    """
    Extended Euclidean Algorithm for finding the modular multiplicative inverse.
    """
    d_old, d_new = 0, 1
    r_old, r_new = phi, e
    while r_new != 0:
        quotient = r_old // r_new
        r_old, r_new = r_new, r_old - quotient * r_new
        d_old, d_new = d_new, d_old - quotient * d_new
    
    if r_old > 1:
        raise ValueError("e is not invertible.")
    if d_old < 0:
        d_old += phi
    
    return d_old

def is_prime(num, test_count=40):
    """
    Miller-Rabin primality test.
    """
    if num == 2 or num == 3:
        return True
    if num <= 1 or num % 2 == 0:
        return False

    s, d = 0, num - 1
    while d % 2 == 0:
        s += 1
        d //= 2

    for _ in range(test_count):
        a = rand.randrange(2, num - 1)
        x = pow(a, d, num)
        if x == 1 or x == num - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, num)
            if x == num - 1:
                break
        else:
            return False
    return True

def generate_prime_candidate(length):
    """
    Generate an odd integer randomly.
    """
    # generate random bits
    p = random.getrandbits(length)
    # apply a mask to set MSB and LSB to 1
    p |= (1 << length - 1) | 1
    return p

def generate_prime_number(length=1024):
    """
    Generate a prime number of length bits.
    """
    p = 4
    while not is_prime(p, 40):
        p = generate_prime_candidate(length)
    return p

def generate_keypair(keysize=1024):
    """
    Generates a public/private key pair.
    Keysize is the bit-length of the RSA modulus n (e.g., 1024, 2048, 4096).
    Returns:
        public_key (e, n), private_key (d, n)
    """
    if keysize < 16 or keysize % 2 != 0:
        raise ValueError("keysize must be an even integer >= 16 (bit-length of modulus n).")

    half = keysize // 2
    p = generate_prime_number(half)
    q = generate_prime_number(half)
    
    # Ensure p and q are distinct
    while p == q:
        q = generate_prime_number(half)
    n = p * q
    phi = (p - 1) * (q - 1)

    # Choose an integer e such that e and phi(n) are coprime
    # Standard choice for e is 65537
    e = 65537
    
    if gcd(e, phi) != 1:
        # Fallback if 65537 is not coprime
        e = random.randrange(2, phi)
        while gcd(e, phi) != 1:
            e = random.randrange(2, phi)

    # Use Extended Euclid's Algorithm to generate the private key
    d = multiplicative_inverse(e, phi)

    return (e, n), (d, n)

def encrypt(public_key, plaintext):
    """
    Encrypts a string into an array of integers using the public key.
    """
    e, n = public_key
    # Convert each character into its numerical ASCII representation,
    # then apply the encryption formula: c = m^e mod n
    cipher = [pow(ord(char), e, n) for char in plaintext]
    return cipher

def decrypt(private_key, ciphertext):
    """
    Decrypts an array of integers into a string using the private key.
    """
    d, n = private_key
    # Apply the decryption formula: m = c^d mod n
    # Convert each integer back to its character equivalent
    plain = [chr(pow(char, d, n)) for char in ciphertext]
    return ''.join(plain)
