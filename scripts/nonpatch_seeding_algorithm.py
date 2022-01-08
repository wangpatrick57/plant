#!/bin/python3

from collections import defaultdict
import sys
import re
from statistics import mean
from odv_helpers import *
from ortholog_helpers import *
from seeding_algorithm_core import *

# settings
MISSING_ALLOWED = 0
MAX_INDICES_FOR_GRAPHLET_ID_ALLOWED = 15
SIMS_MEAN_THRESHOLD = 0.79

# input
k = int(sys.argv[1])
species1 = sys.argv[2]
species2 = sys.argv[3]
s1_index_file_path = sys.argv[4]
s2_index_file_path = sys.argv[5]
which_to_print = sys.argv[6] if len(sys.argv) > 6 else "ORTHO"
s1_odv_file_path = sys.argv[7] if len(sys.argv) > 7 else get_odv_file_path(species1)
s2_odv_file_path = sys.argv[8] if len(sys.argv) > 8 else get_odv_file_path(species2)
speedup = int(sys.argv[9]) if len(sys.argv) > 9 else 1

all_seeds_list = find_seeds(k, species1, species2, s1_index_file_path, s2_index_file_path, s1_odv_file_path, s2_odv_file_path, SeedingAlgorithmSettings())
print('done with finding seeds, now calculating orthoseeds', file=sys.stderr)

# check if it's an orthoseed, according to the amount of MISSING_ALLOWED
s1_to_s2_orthologs = get_s1_to_s2_orthologs(species1, species2)
orthoseeds_list = []

for graphlet_id, s1_index, s2_index in all_seeds_list:
    missing_nodes = 0

    for m in range(k):
        s1_node = s1_index[m]
        s2_node = s2_index[m]

        if s1_node not in s1_to_s2_orthologs or s1_to_s2_orthologs[s1_node] != s2_node:
            missing_nodes += 1

    if missing_nodes <= MISSING_ALLOWED:
        orthoseeds_list.append((graphlet_id, s1_index, s2_index))

# spit out value and percent
pairs_processed = len(all_seeds_list)
list_to_print = orthoseeds_list if which_to_print == "ORTHO" else all_seeds_list
list_to_print_str = '\n'.join(f'{str(graphlet_id)} {",".join(s1_seed)} {",".join(s2_seed)}' for graphlet_id, s1_seed, s2_seed in list_to_print)
print(list_to_print_str)
orthoseed_percent = 0 if pairs_processed == 0 else len(orthoseeds_list) * 100 / pairs_processed
print(f'there are {len(orthoseeds_list)} {k - MISSING_ALLOWED}|{k} orthoseeds out of {pairs_processed} processed graphlet pairs, representing {orthoseed_percent}%', file=sys.stderr)
