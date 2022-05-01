#!/bin/python3
from full_algorithm_helpers import *
from ortholog_helpers import *
from node_to_num_mapping import *

s1_index_path = '/home/wangph1/plant/data/temporal/p0-o0-sxso_start+0shuf_i15M-lDEG2.out'
s2_index_path = '/home/wangph1/plant/data/temporal/p0-o0-sxso_start+5K_i15M-lDEG2.out'
s1_graph_path = '/home/wangph1/plant/networks/temporal_slices/sxso_start+0_inter15000000_shuf.dmel'
s2_graph_path = '/home/wangph1/plant/networks/temporal_slices/sxso_start+5000_inter15000000.dmel'
s1_graph_path = '/home/wangph1/plant/networks/temporal_slices/sxso_start+0_inter15000000_shuf.dmel'
# TODO: s1_to_s2_orthologs
s1_to_s2_orthologs = read_in_n2n('sxso_start+0_i15M', forward=False, convert_to_int=False)
orthopairs, node_pairs = low_param_full_patch_results(s1_index_path, s1_graph_path, s2_index_path, s2_graph_path, s1_to_s2_orthologs)
print('\n'.join([f'{node1}\t{node2}' for node1, node2 in node_pairs]))
