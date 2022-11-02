#!/pkg/python/3.7.4/bin/python3
from all_helpers import *
import sys

for gtag1, gtag2 in get_paper_all_pairs():
    k = two_gtags_to_k(gtag1, gtag2)
    n = two_gtags_to_n(gtag1, gtag2)
    adj_set1 = read_in_adj_set(get_graph_path(gtag1))
    adj_set2 = read_in_adj_set(get_graph_path(gtag2))
    g1_to_g2_ort = get_g1_to_g2_orthologs(gtag1, gtag2)
    out_path = get_mcl_out_path(gtag1, gtag2, k, n, notes='no1')

    if file_exists(out_path):
        m2m_pairs = read_in_slashes_m2m(out_path)
        alignment = extract_big_patch_alignment_from_m2m(m2m_pairs, int(sys.argv[1]), int(sys.argv[2]))
        alignment = get_clean_alignment(alignment, adj_set1, adj_set2)
        size = len(alignment)
        nc = get_alignment_nc(alignment, g1_to_g2_ort, adj_set1, adj_set2)
        s3 = get_s3(alignment, adj_set1, adj_set2)
        print(f'{gtag1}-{gtag2}', size, nc, s3)
        '''alignments = read_in_slashes_alignments(out_path)
        try:
            med_frontier_alignment, size, acc, score = get_med_frontier_alignment(alignments, g1_to_g2_ort, adj_set1, adj_set2)
            # num, max_size = get_mcl_tfp_stats(disjoint_alignments, g1_to_g2_ort, adj_set1, adj_set2)
            print(f'{gtag1}-{gtag2}', size, acc, score)
        except Exception as e:
            print(f'{gtag1}-{gtag2} failed with {e}')'''

    else:
        print(f'{gtag1}-{gtag2}', 'missing')
