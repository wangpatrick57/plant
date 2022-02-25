#!/bin/python3
from patch_helpers import *
from seeding_algorithm_core import *
from ortholog_helpers import *
from node_pair_extraction_helpers import *

species1 = 'syeast0'
species2 = 'syeast25'

all_seeds_list = []

for orbit in range(0, 2):
    k = 10
    s1_index = get_patched_index(8, species1, orbit=orbit)
    s2_index = get_patched_index(8, species2, orbit=orbit)
    # k = 8
    # s1_index = read_in_index(get_index_path(species1, orbit=orbit), k)
    # s2_index = read_in_index(get_index_path(species2 orbit=orbit), k)
    all_seeds = find_seeds(k, species1, species2, s1_index, s2_index, settings=SeedingAlgorithmSettings(max_indices=20, sims_threshold=0.7))
    all_seeds_list.append(all_seeds)
    print(f'done with orbit {orbit}')

combined_seeds = get_combined_seeds_list(all_seeds_list)
all_pairs = extract_node_pairs(combined_seeds)
s1_to_s2_orthologs = get_s1_to_s2_orthologs(species1, species2)
orthopairs = get_orthopairs_list(all_pairs, s1_to_s2_orthologs)
print(f'{len(orthopairs)} / {len(all_pairs)}')
