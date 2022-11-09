#!/pkg/python/3.7.4/bin/python3
from all_helpers import *
import sys

path = sys.argv[1]
alignment = []
gtag1 = 'mouse'
gtag2 = 'rat'

adj_set1 = read_in_adj_set(get_graph_path(gtag1))
adj_set2 = read_in_adj_set(get_graph_path(gtag2))

with open(path) as f:
    for line in f:
        node1, node2 = line.strip().split(',')
        alignment.append((node1, node2))

n = 0
d = 0
        
for i in range(len(alignment)):
    i1 = alignment[i][0]
    i2 = alignment[i][1]
    
    for j in range(i + 1, len(alignment)):
        j1 = alignment[j][0]
        j2 = alignment[j][1]
        
        in1 = j1 in adj_set1[i1]
        in2 = j2 in adj_set2[i2]
        assert (j1 in adj_set1[i1]) == (i1 in adj_set1[j1]), f'{i1}, {j1}'
        assert (j2 in adj_set2[i2]) == (i2 in adj_set2[j2]), f'{i2}, {j2}'

        if in1 or in2:
            d += 1

        if in1 and in2:
            n += 1

print(len(alignment), n, d)
