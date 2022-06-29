#!/pkg/python/3.7.4/bin/python3
from all_helpers import *

path = sys.argv[1]
splitted = path.split('-')
gtag1 = splitted[0]
gtag2 = splitted[1]
adj_set1 = read_in_adj_set(get_graph_path(gtag1))
adj_set2 = read_in_adj_set(get_graph_path(gtag2))

with open(path, 'r') as f:
    for line in f:
        node1, node2, score = line.strip().split()
        node1 = unmark_node(node1)
        node2 = unmark_node(node2)
        deg1 = len(adj_set1[node1])
        deg2 = len(adj_set2[node2])
        print(f'{path}: {node1} ({deg1}), {node2} ({deg2})')
        break
