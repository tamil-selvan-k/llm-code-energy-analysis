import random
import hashlib
from bisect import bisect_left

random.seed(42)
data = sorted(random.randint(0, 10_000_000) for _ in range(1_000_000))
queries = [random.randint(0, 10_000_000) for _ in range(10_000)]
results = []
for q in queries:
    idx = bisect_left(data, q)
    results.append(1 if idx < len(data) and data[idx] == q else 0)
h = hashlib.md5(str(sum(results)).encode()).hexdigest()
print(f"searched {len(queries)} queries in {len(data)} elements, found={sum(results)}, checksum={h}")
