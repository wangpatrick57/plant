#!/bin/python3
from seeding_algorithm_core import *
from blant_cache_helpers import *
from node_pair_extraction_helpers import *
from ortholog_helpers import *

# test constants
k = 8
species1 = "mouse"
species2 = "rat"
lDEG = 2
percent = 0
orbit = 0
sims_thresholds = [n / 100 for n in range(60, 101, 1)]
max_indiceses = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]

for sims_threshold in sims_thresholds:
    orthopairs_results = []
    all_pairs_results = []

    for max_indices in max_indiceses:
        all_seeds_list = find_seeds(k, species1, species2, get_index_path(species1, lDEG=lDEG, percent=percent, orbit=orbit), get_index_path(species2, lDEG=lDEG, percent=percent, orbit=orbit), get_odv_file_path(species1), get_odv_file_path(species2), SeedingAlgorithmSettings(sims_threshold=sims_threshold, max_indices=max_indices), print_progress=False)
        node_pairs = extract_node_pairs(all_seeds_list)
        s1_to_s2_orthologs = get_s1_to_s2_orthologs(species1, species2)
        orthopairs_list = get_orthopairs_list(node_pairs, s1_to_s2_orthologs)
        orthopairs_results.append(len(orthopairs_list))
        all_pairs_results.append(len(node_pairs))

    print('\t'.join([str(result) for result in orthopairs_results]), end='\t\t')
    print('\t'.join([str(result) for result in all_pairs_results]))
