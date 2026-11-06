import hashlib

def sieve_of_eratosthenes(limit):
    is_prime = [True] * (limit + 1)
    is_prime[0] = False
    is_prime[1] = False
    for i in range(2, int(limit ** 0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, limit + 1, i):
                is_prime[j] = False
    primes = []
    for i in range(len(is_prime)):
        if is_prime[i]:
            primes.append(i)
    return primes

primes = sieve_of_eratosthenes(1_000_000)
checksum = hashlib.md5(f"{len(primes)}-{primes[-1]}".encode()).hexdigest()
print(f"found {len(primes)} primes up to 1000000, last={primes[-1]}, checksum={checksum}")
