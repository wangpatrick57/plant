#!/pkg/python/3.7.4/bin/python3
from all_helpers import *
import sys
import os

adj_set1 = read_in_adj_set(get_graph_path('reddit_s0'))
adj_set2 = read_in_adj_set(get_graph_path('reddit_s1'))
print('hamcraft' in adj_set1)
print('hamcraft' in adj_set2)
