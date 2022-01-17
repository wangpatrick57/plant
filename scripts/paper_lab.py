#!/bin/python3
from seeding_algorithm_core import *
from node_pair_extraction_helpers import *
from blant_cache_helpers import *
from odv_helpers import *
from ortholog_helpers import *

all_seeds_lists = []

for orbit in range(0, 15):
    all_seeds_list = find_seeds(8, "mouse", "rat", get_index_path("mouse", orbit=orbit), get_index_path("rat", orbit=orbit), get_odv_file_path("mouse"), get_odv_file_path("rat"), SeedingAlgorithmSettings())
    all_seeds_lists.append(all_seeds_list)
    print(len(all_seeds_list))

combined_seeds = get_combined_seeds_list(all_seeds_lists)
node_pairs = extract_node_pairs(combined_seeds)
s1_to_s2_orthologs = get_s1_to_s2_orthologs("mouse", "rat")
orthopairs_list = get_orthopairs_list(node_pairs, s1_to_s2_orthologs)
print(f'{len(orthopairs_list)} / {len(node_pairs)}')
