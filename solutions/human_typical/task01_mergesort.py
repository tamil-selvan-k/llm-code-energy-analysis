import random
import hashlib

random.seed(42)
numbers = []
for i in range(100_000):
    numbers.append(random.randint(0, 10_000_000))

sorted_numbers = sorted(numbers)

first_100 = sorted_numbers[:100]
checksum = hashlib.md5(str(first_100).encode()).hexdigest()
print(f"sorted {len(sorted_numbers)} elements, checksum={checksum}")
