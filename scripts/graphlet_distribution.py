from collections import defaultdict
import sys

# files
k = int(sys.argv[1])
index_file = open(sys.argv[2], 'r')

# read in human index file
distr = defaultdict(int)

for i, line in enumerate(index_file):
    line_split = line.strip().split()

    if len(line_split) != k + 1:
        print(f'line #{i}, "{line}", does not conform to k{k}')

    graphlet_id = int(line_split[0])
    distr[graphlet_id] += 1

print('\n'.join(f'{gid} {num}' for gid, num in sorted(distr.items(), key = (lambda data : data[0]), reverse = False)))
print(f'total num: {sum(distr.values())}')
