#!/pkg/python/3.7.4/bin/python3
from all_helpers import *

for gtag1, gtag2 in get_paper_all_pairs()[61:]:
    k = two_gtags_to_k(gtag1, gtag2)
    n = two_gtags_to_n(gtag1, gtag2)
    adj_set1 = read_in_adj_set(get_graph_path(gtag1))
    adj_set2 = read_in_adj_set(get_graph_path(gtag2))
    g1_to_g2_ort = get_g1_to_g2_orthologs(gtag1, gtag2)
    out_path = get_mcl_out_path(gtag1, gtag2, k, n, notes='no1')

    if file_exists(out_path):
        alignments = read_in_slashes_alignments(out_path)
        best_scoring_alignment, size, acc, score = get_best_scoring_alignment(alignments, g1_to_g2_ort, adj_set1, adj_set2)
        # num, max_size = get_mcl_tfp_stats(disjoint_alignments, g1_to_g2_ort, adj_set1, adj_set2)
        print(f'{gtag1}-{gtag2}', size, acc, score)
    else:
        print(f'{gtag1}-{gtag2}', 'missing')
