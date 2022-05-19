#!/bin/python3
from seeding_algorithm_core import *
from index_helpers import *
from odv_helpers import *
from node_pair_extraction_helpers import *
from ortholog_helpers import *
from patch_helpers import *

# input parameters (none, since there's only one test right now)

# test constants
k = 8
species1 = "mouse"
species2 = "rat"
percent = 0
max_indices = 15
sims_threshold = 0.74

# run for all orbits
for percent in range(11):
    # run seeding
    s1_index = get_patched_index(k, species1, percent=percent)
    s2_index = get_patched_index(k, species2, percent=percent)
    s1_odv_dir = ODVDirectory(get_odv_dir_path(species1))
    s2_odv_dir = ODVDirectory(get_odv_dir_path(species2))
    seeding_settings = SeedingAlgorithmSettings(max_indices=max_indices, sims_threshold=sims_threshold)
    all_seeds = find_seeds(s1_index, s2_index, s1_odv_dir, s2_odv_dir, settings=seeding_settings)
    all_pairs = extract_node_pairs(all_seeds)
    s1_to_s2 = get_s1_to_s2_orthologs(species1, species2)
    orthopairs = get_orthopairs_list(all_pairs, s1_to_s2)

    # print output immediately
    print(f'{len(orthopairs)}\t{len(all_pairs)}')
