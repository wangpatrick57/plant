#!/bin/python3
from all_helpers import *
import sys
import os

current_k = -1

for gtag1, gtag2 in get_paper_all_pairs():
    pair = f'{gtag1}-{gtag2}'
    
    if gtag2 == 'reddit_s5':
        print(pair, 'skipped')
        continue
    
    adj_set1 = read_in_adj_set(get_graph_path(gtag1))
    adj_set2 = read_in_adj_set(get_graph_path(gtag2))
    g1_to_g2_ort = get_g1_to_g2_orthologs(gtag1, gtag2)
    algo = 'stairs'
    s1_index_path = get_index_path(gtag1, algo=algo)
    s2_index_path = get_index_path(gtag2, algo=algo)
    s1_index = read_in_index(s1_index_path, 8)
    s2_index = read_in_index(s2_index_path, 8)
    
    k = two_gtags_to_k(gtag1, gtag2)
    s1_odv_path = get_odv_path(gtag1, k)
    s2_odv_path = get_odv_path(gtag2, k)
    s1_odv_dir = ODVDirectory(s1_odv_path)
    s2_odv_dir = ODVDirectory(s2_odv_path)
    if k != current_k:
        ODV.set_weights_vars(k)
        current_k = k
    
    seeds = find_seeds(s1_index, s2_index, settings=SeedingAlgorithmSettings(max_indices=15, sims_threshold=0.5), s1_odv_dir=s1_odv_dir, s2_odv_dir=s2_odv_dir)
    alignment = extract_big_patch_alignment_from_seeds(seeds, mindvs=int(sys.argv[1]), minratio=float(sys.argv[2]))
    alignment = get_clean_alignment(alignment, adj_set1, adj_set2)
    nc = get_alignment_nc(alignment, g1_to_g2_ort, adj_set1, adj_set2)
    s3 = get_s3(alignment, adj_set1, adj_set2)
    size = len(alignment)
    print(pair, size, nc, s3)

