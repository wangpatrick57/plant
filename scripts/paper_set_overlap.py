#!/bin/python3
from all_helpers import *
import sys

pairs = get_paper_all_pairs()

for gtag1, gtag2 in pairs:
    k = two_gtags_to_k(gtag1, gtag2)
    n = two_gtags_to_n(gtag1, gtag2)
    to_print = [f'{gtag1}-{gtag2}']

    adj_set1 = read_in_adj_set(get_graph_path(gtag1))
    adj_set2 = read_in_adj_set(get_graph_path(gtag2))
    g1_to_g2_ort = get_g1_to_g2_orthologs(gtag1, gtag2)
    
    algo = 'stairs'
    seeds = raw_full_low_param_run(*get_gtag_run_info(gtag1, gtag2, algo=algo), prox=1)
    bigpatch_alignment = extract_big_patch_alignment_from_seeds(seeds, mindvs=3, minratio=1)
    bigpatch_alignment = get_clean_alignment(bigpatch_alignment, adj_set1, adj_set2)
    bigpatch_nc = get_alignment_nc(bigpatch_alignment, g1_to_g2_ort, adj_set1, adj_set2)
    bigpatch_s3 = get_s3(bigpatch_alignment, adj_set1, adj_set2)

    out_path = get_mcl_out_path(gtag1, gtag2, k, n, notes='no1')
    m2m_pairs = read_in_slashes_m2m(out_path)
    mcl_alignment = extract_big_patch_alignment_from_m2m(m2m_pairs, mindvs=1, minratio=1)
    mcl_alignment = get_clean_alignment(mcl_alignment, adj_set1, adj_set2)
    mcl_nc = get_alignment_nc(mcl_alignment, g1_to_g2_ort, adj_set1, adj_set2)
    mcl_s3 = get_s3(mcl_alignment, adj_set1, adj_set2)

    bigpatch_s1_alignment_set = set([node1 for node1, node2 in bigpatch_alignment])
    mcl_s1_alignment_set = set([node1 for node1, node2 in mcl_alignment])
    s1_set_overlap = len(bigpatch_s1_alignment_set.intersection(mcl_s1_alignment_set))
    bigpatch_s2_alignment_set = set([node2 for node1, node2 in bigpatch_alignment])
    mcl_s2_alignment_set = set([node2 for node1, node2 in mcl_alignment])
    s2_set_overlap = len(bigpatch_s2_alignment_set.intersection(mcl_s2_alignment_set))
    
    to_print.append(len(bigpatch_alignment))
    to_print.append(len(mcl_alignment))
    to_print.append(s1_set_overlap)
    to_print.append(s2_set_overlap)
    to_print.append(bigpatch_nc)
    to_print.append(bigpatch_s3)
    to_print.append(mcl_nc)
    to_print.append(mcl_s3)

    print('\t'.join([str(e) for e in to_print]))
