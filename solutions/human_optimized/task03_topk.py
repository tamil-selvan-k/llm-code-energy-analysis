import random
import hashlib
import heapq

random.seed(42)
data = [random.randint(0, 10_000_000) for _ in range(500_000)]
top100 = heapq.nlargest(100, data)
h = hashlib.md5(str(top100).encode()).hexdigest()
print(f"top 100 from {len(data)} elements, checksum={h}")
