#!/bin/python3
import sys
from patch_helpers import *
from seeding_algorithm_core import *
from ortholog_helpers import *
from node_pair_extraction_helpers import *
from validation_helpers import *
from index_helpers import *
from paper_final_algorithm import *
from general_helpers import *

species1 = 'syeast0'
species2 = sys.argv[1]
patch = sys.argv[2] == 'True'

all_seeds_list = []

edge = find_edge(species1, species2)
threshold = (edge - 10) / 100
print('threshold =', threshold)

for orbit in range(15):
    if not (validate_index_file(get_index_path(species1, orbit=orbit), 8) and validate_index_file(get_index_path(species2, orbit=orbit), 8)):
        continue
    
    s1_index_path = get_index_path(species1, orbit=orbit)
    s2_index_path = get_index_path(species2, orbit=orbit)
    s1_graph_path = get_graph_path(species1)
    s2_graph_path = get_graph_path(species2)

    if patch:
        k = 10
        s1_index = get_patched_index(8, s1_index_path, s1_graph_path)
        s2_index = get_patched_index(8, s2_index_path, s2_graph_path)
    else:
        k = 8
        s1_index = read_in_index(get_index_path(species1, orbit=orbit), k)
        s2_index = read_in_index(get_index_path(species2, orbit=orbit), k)

    s1_odv_dir = ODVDirectory(get_odv_dir_path(species1))
    s2_odv_dir = ODVDirectory(get_odv_dir_path(species2))
    all_seeds = find_seeds(s1_index, s2_index, s1_odv_dir, s2_odv_dir, settings=SeedingAlgorithmSettings(max_indices=8, sims_threshold=threshold))
    all_seeds_list.append(all_seeds)
    print(f'done with orbit {orbit}')

combined_seeds = get_combined_seeds_list(all_seeds_list)
all_pairs = extract_node_pairs(combined_seeds)
s1_to_s2_orthologs = get_s1_to_s2_orthologs(species1, species2)
orthopairs = get_orthopairs_list(all_pairs, s1_to_s2_orthologs)
print(f'{len(orthopairs)} / {len(all_pairs)}')
