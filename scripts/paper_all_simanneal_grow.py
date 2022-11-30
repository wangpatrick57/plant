#!/bin/python3
import sys
from all_helpers import *
from paper_low_k import *

algo = 'stairs'
k = 50000

for gtag1, gtag2 in get_paper_all_pairs()[:2]:
    adj_set1 = read_in_adj_set(get_graph_path(gtag1))
    adj_set2 = read_in_adj_set(get_graph_path(gtag2))
    g1_to_g2_ort = get_g1_to_g2_orthologs(gtag1, gtag2)
    seeds_path = get_seeds_path(gtag1, gtag2, algo=algo, prox=1, target_num_matching=1)
    pair = f'{gtag1}-{gtag2}'

    if os.path.exists(seeds_path):
        seeds = read_in_seeds(seeds_path)
        blocks = seeds_to_blocks(seeds)
        sagrow = SimAnnealGrow(blocks, adj_set1, adj_set2, p_func=ALWAYS_P_FUNC, s3_threshold=1)
        alignment = sagrow.run(k, silent=True)
        alignment = get_clean_alignment(alignment, adj_set1, adj_set2)
        size = len(alignment)
        nc = get_alignment_nc(alignment, g1_to_g2_ort, adj_set1, adj_set2)
        s3 = get_s3(alignment, adj_set1, adj_set2)
        print(pair, size, nc, s3)
    else:
        print(f'{pair} doesn\'t exist')
