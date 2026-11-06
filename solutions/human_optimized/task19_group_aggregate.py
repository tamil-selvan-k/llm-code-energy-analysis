import random
import hashlib
from collections import defaultdict

random.seed(42)
categories = [f"cat_{i}" for i in range(50)]
regions = ['north', 'south', 'east', 'west']
records = [(random.choice(categories), random.choice(regions), random.uniform(10, 1000)) for _ in range(500_000)]

agg = defaultdict(lambda: [0.0, 0, float('inf'), float('-inf')])
for cat, reg, val in records:
    key = (cat, reg)
    a = agg[key]
    a[0] += val
    a[1] += 1
    if val < a[2]: a[2] = val
    if val > a[3]: a[3] = val

result = {k: {"avg": v[0]/v[1], "count": v[1], "min": v[2], "max": v[3]} for k, v in sorted(agg.items())}
h = hashlib.md5(str(len(result)).encode()).hexdigest()
print(f"grouped {len(records)} records into {len(result)} groups, checksum={h}")
