#!/bin/python3
from seeding_algorithm_core import *
from index_helpers import *
from node_pair_extraction_helpers import *
from ortholog_helpers import *
from patch_helpers import *

# test constants
k = 8
patch_k = 10
species1 = "mouse"
species2 = "rat"
percent = 0
orbit = 0
sims_thresholds = [e / 100 for e in list(range(65, 91))]
max_indiceses = list(range(1, 11))
print(sims_thresholds, max_indiceses)

s1_index_path = get_index_path(species1, percent=percent, orbit=orbit)
s2_index_path = get_index_path(species2, percent=percent, orbit=orbit)
s1_graph_path = get_graph_path(species1)
s2_graph_path = get_graph_path(species2)
s1_index = get_patched_index(k, s1_index_path, s1_graph_path)
s2_index = get_patched_index(k, s2_index_path, s2_graph_path)

for sims_threshold in sims_thresholds:
    orthopairs_results = []
    all_pairs_results = []

    for max_indices in max_indiceses:
        all_seeds_list = find_seeds(patch_k, species1, species2, s1_index, s2_index, get_odv_file_path(species1), get_odv_file_path(species2), SeedingAlgorithmSettings(sims_threshold=sims_threshold, max_indices=max_indices), print_progress=False)
        node_pairs = extract_node_pairs(all_seeds_list)
        s1_to_s2_orthologs = get_s1_to_s2_orthologs(species1, species2)
        orthopairs_list = get_orthopairs_list(node_pairs, s1_to_s2_orthologs)
        orthopairs_results.append(len(orthopairs_list))
        all_pairs_results.append(len(node_pairs))

    print('\t'.join([str(result) for result in orthopairs_results]), end='\t\t')
    print('\t'.join([str(result) for result in all_pairs_results]))
