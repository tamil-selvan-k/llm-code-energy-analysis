import random
import hashlib

random.seed(42)
numbers = [random.uniform(1.0, 1_000_000.0) for _ in range(100_000)]

def newton_sqrt(x, tol=1e-10):
    if x == 0:
        return 0.0
    g = x * 0.5
    while True:
        g2 = 0.5 * (g + x / g)
        if abs(g2 - g) < tol:
            return g2
        g = g2

results = [newton_sqrt(n) for n in numbers]
h = hashlib.md5(f"{results[0]:.10f},{results[-1]:.10f}".encode()).hexdigest()
print(f"computed sqrt for {len(numbers)} numbers, checksum={h}")
