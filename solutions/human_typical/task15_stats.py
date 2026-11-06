import random
import hashlib
import math

random.seed(42)
data = [random.gauss(100, 25) for _ in range(1_000_000)]

n = len(data)
total = 0
for x in data:
    total += x
mean = total / n

sum_sq_diff = 0
for x in data:
    sum_sq_diff += (x - mean) ** 2
variance = sum_sq_diff / n
std_dev = math.sqrt(variance)

sum_cube_diff = 0
sum_fourth_diff = 0
for x in data:
    diff = x - mean
    sum_cube_diff += diff ** 3
    sum_fourth_diff += diff ** 4

skewness = (sum_cube_diff / n) / (std_dev ** 3) if std_dev > 0 else 0
kurtosis = (sum_fourth_diff / n) / (std_dev ** 4) - 3 if std_dev > 0 else 0

checksum = hashlib.md5(f"{mean:.6f},{variance:.6f},{std_dev:.6f},{skewness:.6f},{kurtosis:.6f}".encode()).hexdigest()
print(f"stats for {n} values: mean={mean:.4f}, var={variance:.4f}, std={std_dev:.4f}, skew={skewness:.4f}, kurt={kurtosis:.4f}, checksum={checksum}")
