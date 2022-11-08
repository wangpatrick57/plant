#!/pkg/python/3.7.4/bin/python3
# all align means we use all alignments (we may take the frontier to save space)
from all_helpers import *
import sys
from functools import partial

NC = 'nc'
S3 = 's3'

group = sys.argv[1]
acc_type = sys.argv[2]
assert acc_type in [NC, S3]
size_score_points = []

for gtag1, gtag2 in get_group_pairs(group):
    k = two_gtags_to_k(gtag1, gtag2)
    n = two_gtags_to_n(gtag1, gtag2)
    adj_set1 = read_in_adj_set(get_graph_path(gtag1))
    adj_set2 = read_in_adj_set(get_graph_path(gtag2))
    g1_to_g2_ort = get_g1_to_g2_orthologs(gtag1, gtag2)
    out_path = get_mcl_out_path(gtag1, gtag2, k, n, notes='no1')

    if file_exists(out_path):
        alignments = read_in_slashes_alignments(out_path)
        alignments = get_clean_alignments(alignments, adj_set1, adj_set2)
        
        if acc_type == NC:
            frontier_alignments = get_frontier_alignments(alignments, partial(get_alignment_nc, g1_to_g2_ort=g1_to_g2_ort, adj_set1=adj_set1, adj_set2=adj_set2))
        elif acc_type == S3:
            frontier_alignments = get_frontier_alignments(alignments, partial(get_s3, adj_set1=adj_set1, adj_set2=adj_set2))
        else:
            raise AssertionError()
        
        print(f'found {len(frontier_alignments)} frontier alignments for {gtag1}-{gtag2}', file=sys.stderr)

        for alignment, size, score in frontier_alignments:
            size_score_points.append((size, score))
    else:
        print(f'{gtag1}-{gtag2} missing', file=sys.stderr)

    print('\n'.join(f'{size} {score}' for size, score in size_score_points))
