#!/pkg/python/3.7.4/bin/python3
from all_helpers import *

adj_set1 = read_in_adj_set('test1.el')
adj_set2 = read_in_adj_set('test2.el')
alignment1 = [('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')]
alignment2 = [('a', 'E'), ('b', 'F'), ('c', 'G'), ('d', 'H')]
alignment3 = [('a', 'E'), ('b', 'F'), ('c', 'G'), ('e', 'H')]

for alignment in [alignment1, alignment2, alignment3]:
    print()
    print(f'starting {alignment}')
    lca = get_largest_conn_alignment(alignment, adj_set1, adj_set2)
