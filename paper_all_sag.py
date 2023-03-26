#!/bin/python3
from all_helpers import *
from run_sag import get_sag_alignment_path

for gtag1, gtag2 in get_paper_all_pairs():
    adj_set1 = read_in_adj_set(get_graph_path(gtag1))
    adj_set2 = read_in_adj_set(get_graph_path(gtag2))
    g1_to_g2_ort = get_g1_to_g2_orthologs(gtag1, gtag2)
    alignment_path = get_sag_alignment_path(gtag1, gtag2, auto_k=(10000, 0.01))
    alignment = read_in_alignment(alignment_path, adj_set1, adj_set2)
    size = len(alignment)
    nc = get_alignment_nc(alignment, g1_to_g2_ort, adj_set1, adj_set2)
    s3 = get_s3(alignment, adj_set1, adj_set2)
    print(f'{gtag1}-{gtag2}', size, nc, s3, sep='\t')
