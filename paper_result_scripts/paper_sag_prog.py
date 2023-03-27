#!/bin/python3
import sys
from all_helpers import *

gtag1 = sys.argv[1]
gtag2 = sys.argv[2]

algo = 'stairs'
k = 100000
write_every_k = 100
adj_set1 = read_in_adj_set(get_graph_path(gtag1))
adj_set2 = read_in_adj_set(get_graph_path(gtag2))
g1_to_g2_ort = get_g1_to_g2_orthologs(gtag1, gtag2)
seeds_path = get_seeds_path(gtag1, gtag2, algo=algo, prox=1, target_num_matching=1)
pair = f'{gtag1}-{gtag2}'

if os.path.exists(seeds_path):
    seeds = read_in_seeds(seeds_path)
    blocks = seeds_to_blocks(seeds)
    sagrow = SimAnnealGrow(blocks, adj_set1, adj_set2, p_func=ALWAYS_P_FUNC, s3_threshold=1, write_progress_info=(get_data_path(f'simanneal/{gtag1}-{gtag2}-sag_progress.txt'), write_every_k))
    alignment = sagrow.run(k, silent=True)
else:
    print(f'{pair} doesn\'t exist')

