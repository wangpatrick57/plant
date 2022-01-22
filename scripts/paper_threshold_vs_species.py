#!/bin/python3
from seeding_algorithm_core import *
from odv_helpers import *
from blant_cache_helpers import *
from ortholog_helpers import *
from node_pair_extraction_helpers import *

species_pairs = [('human', 'dog'), ('duck', 'horse'), ('fly', 'chicken'), ('cat', 'rat'), ('horse', 'dog')]
MAX_INDICES = int(sys.argv[1])
thresholds = [e / 100 for e in range(65, 90)]
num_orthopairs = []
num_total_nodes = []

for threshold in thresholds:
    num_orthopairs.append([])
    num_total_nodes.append([])
    print(f'starting thresh{threshold}')

    for species1, species2 in species_pairs:
        s1_index_path = get_index_path(species1, 0, 0, 2)
        s2_index_path = get_index_path(species2, 0, 0, 2)
        s1_odv_path = get_odv_file_path(species1)
        s2_odv_path = get_odv_file_path(species2)
        settings = SeedingAlgorithmSettings(MAX_INDICES, threshold, 1)
        all_seeds_list = find_seeds(8, species1, species2, s1_index_path, s2_index_path, s1_odv_path, s2_odv_path, settings)
        all_node_pairs = extract_node_pairs(all_seeds_list)
        s1_to_s2_orthologs = get_s1_to_s2_orthologs(species1, species2)
        orthopairs = get_orthopairs_list(all_node_pairs, s1_to_s2_orthologs)
        num_orthopairs[-1].append(len(orthopairs))
        num_total_nodes[-1].append(len(all_node_pairs))
        print(f'\tdone with thresh{threshold} {species1}-{species2}')

print('orthopairs')

for threshold, threshold_data in zip(thresholds, num_orthopairs):
    print('-'.join([str(threshold)] + [str(e) for e in threshold_data]))

print('all nodes')

for threshold, threshold_data in zip(thresholds, num_total_nodes):
    print('-'.join([str(threshold)] + [str(e) for e in threshold_data]))
