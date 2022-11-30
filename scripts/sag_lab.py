#!/bin/python3
import sys
from all_helpers import *
from paper_low_k import *

gtag1 = sys.argv[1]
gtag2 = sys.argv[2]

algo = 'stairs'
adj_set1 = read_in_adj_set(get_graph_path(gtag1))
adj_set2 = read_in_adj_set(get_graph_path(gtag2))
g1_to_g2_ort = get_g1_to_g2_orthologs(gtag1, gtag2)
seeds_path = get_seeds_path(gtag1, gtag2, algo=algo, prox=1, target_num_matching=1)
pair = f'{gtag1}-{gtag2}'

if os.path.exists(seeds_path):
    seeds = read_in_seeds(seeds_path)
    blocks = seeds_to_blocks(seeds)
    s3_threshold = 0.99
    t_int = int(s3_threshold * 100)
    write_use_block_path = get_data_path(f'simanneal/{gtag1}-{gtag2}-t{t_int}-use_block.txt')

    if s3_threshold == 1:
        read_use_block_path = None
    else:
        old_s3_threshold = s3_threshold + 0.01
        old_t_int = int(old_s3_threshold * 100)
        read_use_block_path = get_data_path(f'simanneal/{gtag1}-{gtag2}-t{old_t_int}-use_block.txt')
        
    sagrow = SimAnnealGrow(blocks, adj_set1, adj_set2, p_func=ALWAYS_P_FUNC, s3_threshold=s3_threshold, read_use_block_path=read_use_block_path)
    alignment = sagrow.run(auto_k=(100, 0.01), silent=False, write_use_block_path=write_use_block_path)
else:
    print(f'{pair} doesn\'t exist')

