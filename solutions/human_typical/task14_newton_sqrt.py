import random
import hashlib

random.seed(42)
numbers = [random.uniform(1.0, 1_000_000.0) for _ in range(100_000)]

def newton_sqrt(x):
    if x == 0:
        return 0
    guess = x / 2.0
    tolerance = 1e-10
    max_iterations = 1000
    for i in range(max_iterations):
        new_guess = (guess + x / guess) / 2.0
        if abs(new_guess - guess) < tolerance:
            return new_guess
        guess = new_guess
    return guess

results = []
for num in numbers:
    results.append(newton_sqrt(num))

checksum = hashlib.md5(f"{results[0]:.10f},{results[-1]:.10f}".encode()).hexdigest()
print(f"computed sqrt for {len(numbers)} numbers, checksum={checksum}")
