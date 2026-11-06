import random
import hashlib
import string

random.seed(42)
text = ''.join(random.choices(string.ascii_lowercase, k=10_000))

def count_palindromes_manacher(s):
    t = '#' + '#'.join(s) + '#'
    n = len(t)
    p = [0] * n
    c = r = 0
    for i in range(n):
        mirror = 2 * c - i
        if i < r:
            p[i] = min(r - i, p[mirror])
        while i + p[i] + 1 < n and i - p[i] - 1 >= 0 and t[i + p[i] + 1] == t[i - p[i] - 1]:
            p[i] += 1
        if i + p[i] > r:
            c, r = i, i + p[i]
    count = sum((v + 1) // 2 for v in p)
    return count

count = count_palindromes_manacher(text)
h = hashlib.md5(str(count).encode()).hexdigest()
print(f"found {count} palindromic substrings in {len(text)} chars, checksum={h}")
