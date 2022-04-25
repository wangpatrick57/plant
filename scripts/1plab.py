#!/bin/python3
import sys
from full_algorithm_helpers import *
from ortholog_helpers import *

index_name = sys.argv[1]
graph_name = sys.argv[2]

index_base_dir = '/home/wangph1/plant/data/temporal'
s1_index_path = f'{index_base_dir}/p0-o0-sxso_start+0_i15M-lDEG2.out'
s2_index_path = f'{index_base_dir}/p0-o0-sxso_start+{index_name}_i15M-lDEG2.out'

graph_base_dir = '/home/wangph1/plant/networks/temporal_slices'
s1_graph_path = f'{graph_base_dir}/sxso_start+0_inter15000000.el'
s2_graph_path = f'{graph_base_dir}/sxso_start+{graph_name}_inter15000000.el'

s1_to_s2_orthologs = SelfOrthos()
orthopairs, node_pairs = low_param_full_patch_results(s1_index_path, s1_graph_path, s2_index_path, s2_graph_path, s1_to_s2_orthologs)
print(f'{len(orthopairs)} / {len(node_pairs)}')
