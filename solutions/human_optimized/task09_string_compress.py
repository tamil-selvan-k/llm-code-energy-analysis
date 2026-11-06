import random
import hashlib
import string
from itertools import groupby

random.seed(42)
text = ''.join(random.choices(string.ascii_lowercase[:5], k=1_000_000))
compressed = ''.join(f"{ch}{sum(1 for _ in grp)}" for ch, grp in groupby(text))
h = hashlib.md5(compressed[:1000].encode()).hexdigest()
print(f"compressed {len(text)} -> {len(compressed)} chars, checksum={h}")
