#!/pkg/python/3.7.4/bin/python3
import sys
from full_algorithm_helpers import *
from index_helpers import *
from graph_helpers import *
from ortholog_helpers import *

snap1 = sys.argv[1]
snap2 = sys.argv[2]
s1_index_path = get_index_path(snap1)
s1_graph_path = get_graph_path(snap1)
s2_index_path = get_index_path(snap2)
s2_graph_path = get_graph_path(snap2)
s1_to_s2_orthologs = SelfOrthos()

orth = []
total = []

for prox in range(1, 11):
    orth.append([])
    total.append([])

    for target_num_matching in range(1, 8):
        orthopairs, node_pairs = low_param_full_patch_results(s1_index_path, s1_graph_path, s2_index_path, s2_graph_path, s1_to_s2_orthologs, prox=prox, target_num_matching=target_num_matching)
        orth[-1].append(len(orthopairs))
        total[-1].append(len(node_pairs))
        print(f'done with t{target_num_matching} p{prox}')

print('orth')
print('\n'.join(['\t'.join([f'{num}' for num in row]) for row in orth]))
print()
print('total')
print('\n'.join(['\t'.join([f'{num}' for num in row]) for row in total]))
