#!/pkg/python/3.7.4/bin/python3
from all_helpers import *
import sys

notes = sys.argv[1]
bnstr = '2B'
pairs = get_syeast_pairs()

for k in [5, 6]:
    for gtag1, gtag2 in pairs:
        n = two_gtags_to_n(gtag1, gtag2)
        to_print = [f'{gtag1}-{gtag2}', f'{k}']
        path = get_odv_ort_path(gtag1, gtag2, k, n, bnstr=bnstr, notes=notes)

        try:
            odv_orts = read_in_odv_orts(path, include_score=False)
        except:
            print(f'{gtag1}-{gtag2} doesn\'t exist')
            continue

        adj_set1 = read_in_adj_set(get_graph_path(gtag1))
        adj_set2 = read_in_adj_set(get_graph_path(gtag2))
        alignment = make_odv_ort_1to1(odv_orts)
        # alignment = get_clean_alignment(alignment, adj_set1, adj_set2)
        g1_to_g2_ort = get_g1_to_g2_orthologs(gtag1, gtag2)
        nc = get_alignment_nc(alignment, g1_to_g2_ort, adj_set1, adj_set2)
        s3 = get_s3(alignment, adj_set1, adj_set2)
        to_print.append(len(alignment))
        to_print.append(nc)
        to_print.append(s3)

        print('\t'.join([str(e) for e in to_print]))
