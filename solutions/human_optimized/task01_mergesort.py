import random
import hashlib

random.seed(42)
data = [random.randint(0, 10_000_000) for _ in range(100_000)]
data.sort()
h = hashlib.md5(str(data[:100]).encode()).hexdigest()
print(f"sorted {len(data)} elements, checksum={h}")
