#!/bin/python3
from seeding_algorithm_core import *
from node_pair_extraction_helpers import *
from blant_cache_helpers import *
from odv_helpers import *
from ortholog_helpers import *

all_seeds_list = find_seeds(8, "mouse", "rat", get_index_path("mouse"), get_index_path("rat"), get_odv_file_path("mouse"), get_odv_file_path("rat"), SeedingAlgorithmSettings())
node_pairs = extract_node_pairs(all_seeds_list)
s1_to_s2_orthologs = get_s1_to_s2_orthologs("mouse", "rat")
orthopairs_list = get_orthopairs_list(node_pairs, s1_to_s2_orthologs)
print(len(orthopairs_list))
print(len(node_pairs))
