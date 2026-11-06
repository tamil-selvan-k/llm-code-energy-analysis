import random
import hashlib
import io
import csv

random.seed(42)
departments = ['eng', 'sales', 'hr', 'ops', 'mktg']

lines = ['id,dept,salary,age']
for i in range(100_000):
    dept = random.choice(departments)
    salary = random.randint(30000, 200000)
    age = random.randint(22, 65)
    lines.append(f"{i},{dept},{salary},{age}")

csv_text = '\n'.join(lines)
reader = csv.DictReader(io.StringIO(csv_text))

dept_salaries = {}
dept_counts = {}
for row in reader:
    dept = row['dept']
    salary = int(row['salary'])
    if dept not in dept_salaries:
        dept_salaries[dept] = 0
        dept_counts[dept] = 0
    dept_salaries[dept] += salary
    dept_counts[dept] += 1

averages = {}
for dept in sorted(dept_salaries.keys()):
    averages[dept] = dept_salaries[dept] / dept_counts[dept]

checksum = hashlib.md5(str(averages).encode()).hexdigest()
print(f"parsed 100K rows, {len(averages)} departments, checksum={checksum}")
