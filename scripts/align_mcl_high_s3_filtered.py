#!/pkg/python/3.7.4/bin/python3
from all_helpers import *
import sys
from functools import partial

if __name__ == '__main__':
    pairs = get_iid_mammal_pairs()

    for gtag1, gtag2 in pairs:
        k = two_gtags_to_k(gtag1, gtag2)
        n = two_gtags_to_n(gtag1, gtag2)
        adj_set1 = read_in_adj_set(get_graph_path(gtag1))
        adj_set2 = read_in_adj_set(get_graph_path(gtag2))
        g1_to_g2_ort = get_g1_to_g2_orthologs(gtag1, gtag2)
        out_path = get_mcl_out_path(gtag1, gtag2, k, n, notes='no1')

        if file_exists(out_path):
            alignments = read_in_slashes_alignments(out_path)
            alignments = get_clean_alignments(alignments, adj_set1, adj_set2)
            filtered_alignments = get_s3_filtered_alignments(alignments, adj_set1, adj_set2)

            for filtered_alignment in filtered_alignments:
                nc = get_alignment_nc(filtered_alignment, g1_to_g2_ort, adj_set1, adj_set2)
                s3 = get_s3(filtered_alignment, adj_set1, adj_set2)

                if len(filtered_alignment) >= 10:
                    print(f'{gtag1}-{gtag2}', len(filtered_alignment), nc, s3, sep='\t')
        else:
            print(f'{gtag1}-{gtag2} missing', file=sys.stderr)
