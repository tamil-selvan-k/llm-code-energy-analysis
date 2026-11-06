import random
import hashlib

random.seed(42)
data = [random.randint(0, 10_000_000) for _ in range(500_000)]
sorted_data = sorted(data)
n = len(sorted_data)
if n % 2 == 0:
    median = (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2
else:
    median = sorted_data[n // 2]
checksum = hashlib.md5(str(median).encode()).hexdigest()
print(f"median of {len(data)} elements = {median}, checksum={checksum}")
