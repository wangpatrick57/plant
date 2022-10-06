#!/pkg/python/3.7.4/bin/python3
from all_helpers import *
import sys

path1 = get_custom_graph_path("hammer4")
adj_set1 = read_in_adj_set(path1)
path2 = get_custom_graph_path("clique5")
adj_set2 = read_in_adj_set(path2)
alignment1 = [('0', '0'), ('1', '1'), ('2', '2'), ('3', '3')]
print(get_s3(alignment1, adj_set1, adj_set2))

path1 = get_custom_graph_path("hammer4")
adj_set1 = read_in_adj_set(path1)
path2 = get_custom_graph_path("virus5")
adj_set2 = read_in_adj_set(path2)
alignment1 = [('0', '0'), ('1', '1'), ('2', '2'), ('3', '3')]
print(get_s3(alignment1, adj_set1, adj_set2))

path1 = get_custom_graph_path("hammer4")
adj_set1 = read_in_adj_set(path1)
path2 = get_custom_graph_path("bighammer5")
adj_set2 = read_in_adj_set(path2)
alignment1 = [('0', '0'), ('1', '1'), ('2', '2'), ('3', '3')]
print(get_s3(alignment1, adj_set1, adj_set2))
