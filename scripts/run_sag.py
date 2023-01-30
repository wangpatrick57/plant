#!/bin/python3
import sys
from all_helpers import *

def get_sag_alignment_path(gtag1, gtag2, auto_k=None):
    return get_data_path(f'simanneal/{gtag1}-{gtag2}-w{auto_k[0]}-p{int(auto_k[1] * 100)}.align')

if __name__ == '__main__':
    gtag1 = sys.argv[1]
    gtag2 = sys.argv[2]

    algo = 'stairs'
    auto_k = (10000, 0.01)
    adj_set1 = read_in_adj_set(get_graph_path(gtag1))
    adj_set2 = read_in_adj_set(get_graph_path(gtag2))
    g1_to_g2_ort = get_g1_to_g2_orthologs(gtag1, gtag2)
    seeds_path = get_seeds_path(gtag1, gtag2, algo=algo, prox=1, target_num_matching=1)
    sag_alignment_path = get_sag_alignment_path(gtag1, gtag2, auto_k=auto_k)
    time_path = '.'.join(sag_alignment_path.split('.')[:-1]) + '.time'
    pair = f'{gtag1}-{gtag2}'

    if os.path.exists(seeds_path):
        if os.path.exists(sag_alignment_path):
            alignment = read_in_alignment(sag_alignment_path, adj_set1, adj_set2)
        else:
            start_time = time.time()
            seeds = read_in_seeds(seeds_path)
            blocks = seeds_to_blocks(seeds)
            sagrow = SimAnnealGrow(blocks, adj_set1, adj_set2, p_func=ALWAYS_P_FUNC, s3_threshold=1)
            alignment = sagrow.run(auto_k=auto_k, silent=False)
            alignment = get_clean_alignment(alignment, adj_set1, adj_set2)
            end_time = time.time()
            write_to_file(alignment_to_str(alignment), sag_alignment_path)
            write_to_file(f'{end_time - start_time}', time_path)

        size = len(alignment)
        nc = get_alignment_nc(alignment, g1_to_g2_ort, adj_set1, adj_set2)
        s3 = get_s3(alignment, adj_set1, adj_set2)
        print(pair, size, nc, s3)
    else:
        print(f'{pair} doesn\'t exist')
