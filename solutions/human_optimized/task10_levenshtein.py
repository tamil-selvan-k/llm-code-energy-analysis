import random
import hashlib
import string

random.seed(42)
pairs = [(''.join(random.choices(string.ascii_lowercase, k=random.randint(80, 120))),
          ''.join(random.choices(string.ascii_lowercase, k=random.randint(80, 120))))
         for _ in range(500)]

def lev(a, b):
    if len(a) < len(b):
        a, b = b, a
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        curr = [i] + [0] * len(b)
        for j, cb in enumerate(b, 1):
            curr[j] = min(prev[j] + 1, curr[j-1] + 1, prev[j-1] + (ca != cb))
        prev = curr
    return prev[-1]

dists = [lev(a, b) for a, b in pairs]
total = sum(dists)
h = hashlib.md5(str(total).encode()).hexdigest()
print(f"computed {len(pairs)} edit distances, total={total}, checksum={h}")
