#!/pkg/python/3.7.4/bin/python3
from all_helpers import *
import sys
import os

for gtag1, gtag2 in get_paper_all_pairs():
    pair = f'{gtag1}-{gtag2}'
    
    if gtag2 == 'reddit_s5':
        print(pair, 'skipped')
        continue
    
    adj_set1 = read_in_adj_set(get_graph_path(gtag1))
    adj_set2 = read_in_adj_set(get_graph_path(gtag2))
    g1_to_g2_ort = get_g1_to_g2_orthologs(gtag1, gtag2)
    algo = 'stairs'
    seeds = raw_full_low_param_run(*get_gtag_run_info(gtag1, gtag2, algo=algo), prox=1)
    alignment = extract_big_patch_alignment_from_seeds(seeds, mindvs=int(sys.argv[1]), minratio=float(sys.argv[2]))
    alignment = get_clean_alignment(alignment, adj_set1, adj_set2)
    size = len(alignment)
    nc = get_alignment_nc(alignment, g1_to_g2_ort, adj_set1, adj_set2)
    s3 = get_s3(alignment, adj_set1, adj_set2)
    print(pair, size, nc, s3)
