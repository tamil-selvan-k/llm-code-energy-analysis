import random
import hashlib

random.seed(42)
data = [random.randint(0, 10_000_000) for _ in range(500_000)]
sorted_data = sorted(data, reverse=True)
top100 = sorted_data[:100]
checksum = hashlib.md5(str(top100).encode()).hexdigest()
print(f"top 100 from {len(data)} elements, checksum={checksum}")
