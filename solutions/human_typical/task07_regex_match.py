import random
import hashlib
import re
import string

random.seed(42)
lines = []
for _ in range(100_000):
    length = random.randint(20, 100)
    line = ''.join(random.choices(string.ascii_lowercase + string.digits + ' ', k=length))
    lines.append(line)

pattern1 = r'\b[a-z]{5}\d{3}\b'
pattern2 = r'[aeiou]{3,}'
pattern3 = r'\d{2,4}[a-z]+\d'

count1 = 0
count2 = 0
count3 = 0

for line in lines:
    if re.search(pattern1, line):
        count1 += 1
    if re.search(pattern2, line):
        count2 += 1
    if re.search(pattern3, line):
        count3 += 1

counts = [count1, count2, count3]
checksum = hashlib.md5(str(counts).encode()).hexdigest()
print(f"matched patterns in {len(lines)} lines, counts={counts}, checksum={checksum}")
