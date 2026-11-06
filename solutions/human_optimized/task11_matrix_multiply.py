import random
import hashlib

random.seed(42)
N = 300
A = [[random.random() for _ in range(N)] for _ in range(N)]
B = [[random.random() for _ in range(N)] for _ in range(N)]

BT = list(zip(*B))
C = [[sum(a * b for a, b in zip(row_a, col_b)) for col_b in BT] for row_a in A]

h = hashlib.md5(f"{C[0][0]:.6f},{C[N-1][N-1]:.6f}".encode()).hexdigest()
print(f"multiplied {N}x{N} matrices, checksum={h}")
