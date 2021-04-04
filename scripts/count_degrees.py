from collections import defaultdict
import sys

degrees = defaultdict(int)

for line in open(sys.argv[1], 'r'):
    line = line.strip()
    a, b = line.split(' ')
    degrees[a] += 1
    degrees[b] += 1

print(degrees.values())
