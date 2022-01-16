#!/bin/python3
from seeding_algorithm_core import *
from blant_cache_helpers import *
from odv_helpers import *
from node_pair_extraction_helpers import *
from ortholog_helpers import *

# input parameters (none, since there's only one test right now)

# test constants
k = 8
species1 = "mouse"
species2 = "rat"
lDEG = 2
percent = 0
max_indices = 15
sims_threshold = 0.79

# run for all orbits
for orbit in range(0, 15):
    # run seeding
    s1_index_path = get_index_path(species1, percent=percent, orbit=orbit, lDEG=lDEG)
    s2_index_path = get_index_path(species2, percent=percent, orbit=orbit, lDEG=lDEG)
    s1_odv_path = get_odv_file_path(species1)
    s2_odv_path = get_odv_file_path(species2)
    seeding_settings = SeedingAlgorithmSettings(max_indices=max_indices, sims_threshold=sims_threshold)
    all_seeds = find_seeds(k, species1, species2, s1_index_path, s2_index_path, s1_odv_path, s2_odv_path, seeding_settings)

    # extract pairs
    all_pairs = extract_node_pairs(all_seeds)

    # calculate orthopairs
    s1_to_s2_orthologs = get_s1_to_s2_orthologs(species1, species2)
    orthopairs = get_orthopairs_list(all_pairs, s1_to_s2_orthologs)

    # print output immediately
    print(f'{len(orthopairs)}\t{len(all_pairs)}')
