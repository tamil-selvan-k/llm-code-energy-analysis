import hashlib

def sieve(n):
    is_prime = bytearray(b'\x01') * (n + 1)
    is_prime[0] = is_prime[1] = 0
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            is_prime[i*i::i] = bytearray(len(is_prime[i*i::i]))
    return [i for i, v in enumerate(is_prime) if v]

primes = sieve(1_000_000)
h = hashlib.md5(f"{len(primes)}-{primes[-1]}".encode()).hexdigest()
print(f"found {len(primes)} primes up to 1000000, last={primes[-1]}, checksum={h}")
