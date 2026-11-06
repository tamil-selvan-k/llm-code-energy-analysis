"""
Task 16: CSV Parsing and Aggregation Benchmark
Parses a generated 100K-row CSV and computes average salary per department.
"""

import random
import hashlib
import io
import csv
from typing import Dict, List
from collections import defaultdict
from dataclasses import dataclass, field


@dataclass
class DepartmentStatistics:
    """Aggregated statistics for a department."""
    total_salary: int = 0
    employee_count: int = 0

    def add_employee(self, salary: int) -> None:
        """Add an employee's salary to the department statistics."""
        self.total_salary += salary
        self.employee_count += 1

    def get_average_salary(self) -> float:
        """Calculate average salary."""
        if self.employee_count == 0:
            return 0.0
        return self.total_salary / self.employee_count


def generate_csv_data(num_rows: int, seed: int = 42) -> str:
    """Generate CSV data with employee records."""
    if num_rows <= 0:
        raise ValueError("Number of rows must be positive")

    random.seed(seed)
    departments = ['eng', 'sales', 'hr', 'ops', 'mktg']

    output_buffer = io.StringIO()
    csv_writer = csv.writer(output_buffer)
    csv_writer.writerow(['id', 'dept', 'salary', 'age'])

    for employee_id in range(num_rows):
        department = random.choice(departments)
        salary = random.randint(30000, 200000)
        age = random.randint(22, 65)
        csv_writer.writerow([employee_id, department, salary, age])

    return output_buffer.getvalue()


def parse_and_aggregate_csv(csv_data: str) -> Dict[str, float]:
    """Parse CSV data and compute average salary per department."""
    reader = csv.DictReader(io.StringIO(csv_data))
    department_stats: Dict[str, DepartmentStatistics] = {}

    for row in reader:
        department_name = row['dept']
        employee_salary = int(row['salary'])

        if department_name not in department_stats:
            department_stats[department_name] = DepartmentStatistics()

        department_stats[department_name].add_employee(employee_salary)

    average_salaries = {}
    for dept_name in sorted(department_stats.keys()):
        stats = department_stats[dept_name]
        average_salaries[dept_name] = stats.get_average_salary()

    return average_salaries


def main():
    """Main function."""
    num_rows = 100_000
    csv_data = generate_csv_data(num_rows)
    averages = parse_and_aggregate_csv(csv_data)
    checksum = hashlib.md5(str(averages).encode()).hexdigest()
    print(f"parsed {num_rows} rows, {len(averages)} departments, checksum={checksum}")


if __name__ == "__main__":
    main()
