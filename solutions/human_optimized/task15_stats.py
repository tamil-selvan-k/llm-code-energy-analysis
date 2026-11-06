import random
import hashlib
import math

random.seed(42)
data = [random.gauss(100, 25) for _ in range(1_000_000)]
n = len(data)
mean = sum(data) / n
var = sum((x - mean) ** 2 for x in data) / n
std = math.sqrt(var)
m3 = sum((x - mean) ** 3 for x in data) / n
m4 = sum((x - mean) ** 4 for x in data) / n
skew = m3 / (std ** 3) if std else 0
kurt = m4 / (std ** 4) - 3 if std else 0
h = hashlib.md5(f"{mean:.6f},{var:.6f},{std:.6f},{skew:.6f},{kurt:.6f}".encode()).hexdigest()
print(f"stats for {n} values: mean={mean:.4f}, var={var:.4f}, std={std:.4f}, skew={skew:.4f}, kurt={kurt:.4f}, checksum={h}")
