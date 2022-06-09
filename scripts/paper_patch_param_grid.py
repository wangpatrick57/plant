#!/pkg/python/3.7.4/bin/python3
import sys
from full_algorithm_helpers import *
from index_helpers import *
from graph_helpers import *
from ortholog_helpers import *

gtag1 = sys.argv[1]
gtag2 = sys.argv[2]
algo = 'bno'
s1_index_path = get_index_path(gtag1, algo=algo)
s1_graph_path = get_graph_path(gtag1)
s2_index_path = get_index_path(gtag2, algo=algo)
s2_graph_path = get_graph_path(gtag2)
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
