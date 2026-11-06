import random
import hashlib

random.seed(42)
categories = [f"cat_{i}" for i in range(50)]
regions = ['north', 'south', 'east', 'west']

records = []
for _ in range(500_000):
    cat = random.choice(categories)
    reg = random.choice(regions)
    val = random.uniform(10, 1000)
    records.append((cat, reg, val))

groups = {}
for cat, reg, val in records:
    key = (cat, reg)
    if key not in groups:
        groups[key] = []
    groups[key].append(val)

result = {}
for key in sorted(groups.keys()):
    values = groups[key]
    avg = sum(values) / len(values)
    result[key] = {
        "avg": avg,
        "count": len(values),
        "min": min(values),
        "max": max(values)
    }

checksum = hashlib.md5(str(len(result)).encode()).hexdigest()
print(f"grouped {len(records)} records into {len(result)} groups, checksum={checksum}")
