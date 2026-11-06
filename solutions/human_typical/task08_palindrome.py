import random
import hashlib
import string

random.seed(42)
text = ''.join(random.choices(string.ascii_lowercase, k=10_000))

def expand_around_center(s, left, right):
    count = 0
    while left >= 0 and right < len(s) and s[left] == s[right]:
        count += 1
        left -= 1
        right += 1
    return count

total = 0
for i in range(len(text)):
    total += expand_around_center(text, i, i)
    total += expand_around_center(text, i, i + 1)

checksum = hashlib.md5(str(total).encode()).hexdigest()
print(f"found {total} palindromic substrings in {len(text)} chars, checksum={checksum}")
