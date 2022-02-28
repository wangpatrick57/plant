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
    
    if patch:
        k = 10
        s1_index = get_patched_index(8, species1, orbit=orbit)
        s2_index = get_patched_index(8, species2, orbit=orbit)
    else:
        k = 8
        s1_index = read_in_index(get_index_path(species1, orbit=orbit), k)
        s2_index = read_in_index(get_index_path(species2, orbit=orbit), k)

    all_seeds = find_seeds(k, species1, species2, s1_index, s2_index, settings=SeedingAlgorithmSettings(max_indices=25, sims_threshold=threshold))
    all_seeds_list.append(all_seeds)
    print(f'done with orbit {orbit}')

combined_seeds = get_combined_seeds_list(all_seeds_list)
all_pairs = extract_node_pairs(combined_seeds)
s1_to_s2_orthologs = get_s1_to_s2_orthologs(species1, species2)
orthopairs = get_orthopairs_list(all_pairs, s1_to_s2_orthologs)
print(f'{len(orthopairs)} / {len(all_pairs)}')
