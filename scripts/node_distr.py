import sys
from collections import defaultdict

el_file = open(sys.argv[1], 'r')
node_distr = defaultdict(int)

for line in el_file:
    l, r = line.strip().split()
    node_distr[l] += 1
    node_distr[r] += 1

count_distr = defaultdict(int)

for node, count in node_distr.items():
    count_distr[count] += 1

print('\n'.join([f'{count} {appearances}' for count, appearances in count_distr.items()]))
