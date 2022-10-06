#!/pkg/python/3.7.4/bin/python3
from all_helpers import *
import sys

path1 = get_custom_graph_path("hammer4")
adj_set1 = read_in_adj_set(path1)
path2 = get_custom_graph_path("clique5")
adj_set2 = read_in_adj_set(path2)
alignment1 = [(0, 0), (1, 1), (2, 2), (3, 3)]
print(get_s3(alignment1, adj_set1, adj_set2))
alignment2 = [(0, 0), (1, 1), (2, 2), (3, 3), (0, 0), (1, 1)]
print(get_s3(alignment2, adj_set1, adj_set2))
alignment3 = [(0, 0), (4, 1), (1, 1), (2, 2), (3, 3), (3, 4)]
print(get_s3(alignment3, adj_set1, adj_set2))
alignment4 = [(0, 0), (4, 1), (1, 1), (2, 2), (3, 3), (3, 4), (3, 4)]
print(get_s3(alignment4, adj_set1, adj_set2))
alignment5 = [(0, 0), (4, 1), (1, 1), (2, 2), (3, 3), (3, 4), (0, 0)]
print(get_s3(alignment5, adj_set1, adj_set2))
