#!/pkg/python/3.7.4/bin/python3
from all_helpers import *
import sys
import os

for gtag1, gtag2 in get_paper_all_pairs()[60:]:
    pair = f'{gtag1}-{gtag2}'
    adj_set1 = read_in_adj_set(get_graph_path(gtag1))
    adj_set2 = read_in_adj_set(get_graph_path(gtag2))
    g1_to_g2_ort = get_g1_to_g2_orthologs(gtag1, gtag2)
    algo = 'bno'
    seeds, _, _ = simplified_run_with_metrics(gtag1, gtag2, algo=algo, silent=True)
    alignment = extract_big_patch_alignment(seeds, mindvs=int(sys.argv[1]), minratio=float(sys.argv[2]))
    nc = get_alignment_nc(alignment, g1_to_g2_ort)
    s3 = get_s3(alignment, adj_set1, adj_set2)
    size = len(alignment)
    print(pair, size, nc, s3)
