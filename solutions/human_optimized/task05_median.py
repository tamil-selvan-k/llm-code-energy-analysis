import random
import hashlib
import statistics

random.seed(42)
data = [random.randint(0, 10_000_000) for _ in range(500_000)]
med = statistics.median(data)
h = hashlib.md5(str(med).encode()).hexdigest()
print(f"median of {len(data)} elements = {med}, checksum={h}")
