#!/bin/python3
from node_pair_extraction_helpers import *
from seeding_algorithm_core import *
from index_helpers import *
from odv_helpers import *
from ortholog_helpers import *
from file_helpers import *

# setup
k = 8
patch_k = 10
species1 = 'mouse'
species2 = 'rat'
s1_index = get_patched_index(k, species1)
s2_index = get_patched_index(k, species2)
s1_notopedge_index_path = get_notopedge_index_path(species1)
s2_notopedge_index_path = get_notopedge_index_path(species2)
s1_notopedge_index = read_in_index(s1_notopedge_index_path, k)
s2_notopedge_index = read_in_index(s2_notopedge_index_path, k)
s1_odv_path = get_odv_file_path(species1)
s2_odv_path = get_odv_file_path(species2)
settings = SeedingAlgorithmSettings(max_indices=15, sims_threshold=0.79, speedup=1)
s1_to_s2_orthologs = get_s1_to_s2_orthologs(species1, species2)

# both normal
allseeds = find_seeds(k, species1, species2, s1_index, s2_index, s1_odv_path, s2_odv_path, settings, print_progress=False)
allpairs = extract_node_pairs(allseeds)
orthopairs = get_orthopairs_list(allpairs, s1_to_s2_orthologs)
print(f'both normal: {len(orthopairs)} / {len(allpairs)}')

# mouse notopedge, rat normal
allseeds = find_seeds(k, species1, species2, s1_notopedge_index, s2_index, s1_odv_path, s2_odv_path, settings, print_progress=False)
allpairs = extract_node_pairs(allseeds)
orthopairs = get_orthopairs_list(allpairs, s1_to_s2_orthologs)
print(f'both normal: {len(orthopairs)} / {len(allpairs)}')

# mouse normal, rat notopedge
allseeds = find_seeds(k, species1, species2, s1_index, s2_notopedge_index, s1_odv_path, s2_odv_path, settings, print_progress=False)
allpairs = extract_node_pairs(allseeds)
orthopairs = get_orthopairs_list(allpairs, s1_to_s2_orthologs)
print(f'both normal: {len(orthopairs)} / {len(allpairs)}')

# both notopedge
allseeds = find_seeds(k, species1, species2, s1_notopedge_index, s2_notopedge_index, s1_odv_path, s2_odv_path, settings, print_progress=False)
allpairs = extract_node_pairs(allseeds)
orthopairs = get_orthopairs_list(allpairs, s1_to_s2_orthologs)
print(f'both normal: {len(orthopairs)} / {len(allpairs)}')
