#!/bin/python3
from full_algorithm_helpers import *
from selector_helpers import *
from graph_helpers import *

s1_index_path = IndexSelector(by_blant_settings={'species': 'mouse'}).get_path()
s2_index_path = IndexSelector(by_blant_settings={'species': 'rat'}).get_path()
s1_graph_path = get_graph_path('mouse')
s2_graph_path = get_graph_path('rat')
s1_to_s2_orthologs = get_s1_to_s2_orthologs('mouse', 'rat')
orthopairs, node_pairs = low_param_full_patch_results(s1_index_path, s1_graph_path, s2_index_path, s2_graph_path, s1_to_s2_orthologs)

print(f'{len(orthopairs)} / {len(node_pairs)}')
print(orthopairs)
