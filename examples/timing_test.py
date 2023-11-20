import time

from FuzzyMath import FuzzyNumberFactory

time_start = time.time()
fns = []

for i in range(1_000_000):
    fns.append(FuzzyNumberFactory.triangular(i - 1, i, i + 1, 10))

print(time.time() - time_start)

time_start = time.time()

result = FuzzyNumberFactory.crisp_number(0)

for fn in fns:
    result = result + fn

print(time.time() - time_start)
print(result)
