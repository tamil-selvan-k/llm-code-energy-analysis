import random
import hashlib
import io
import csv
from collections import defaultdict

random.seed(42)
departments = ['eng', 'sales', 'hr', 'ops', 'mktg']
buf = io.StringIO()
w = csv.writer(buf)
w.writerow(['id', 'dept', 'salary', 'age'])
for i in range(100_000):
    w.writerow([i, random.choice(departments), random.randint(30000, 200000), random.randint(22, 65)])

buf.seek(0)
reader = csv.DictReader(buf)
agg = defaultdict(lambda: [0, 0])
for row in reader:
    d = row['dept']
    agg[d][0] += int(row['salary'])
    agg[d][1] += 1

result = {d: v[0] / v[1] for d, v in sorted(agg.items())}
h = hashlib.md5(str(result).encode()).hexdigest()
print(f"parsed 100K rows, {len(result)} departments, checksum={h}")
