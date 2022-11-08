#!/pkg/python/3.7.4/bin/python3
from all_helpers import *
import sys
from functools import partial

gtag1 = 'mouse'
gtag2 = 'rat'
k = two_gtags_to_k(gtag1, gtag2)
n = two_gtags_to_n(gtag1, gtag2)
adj_set1 = read_in_adj_set(get_graph_path(gtag1))
adj_set2 = read_in_adj_set(get_graph_path(gtag2))
g1_to_g2_ort = get_g1_to_g2_orthologs(gtag1, gtag2)
out_path = get_mcl_out_path(gtag1, gtag2, k, n, notes='no1')
alignments = read_in_slashes_alignments(out_path)
alignments = get_clean_alignments(alignments, adj_set1, adj_set2)
frontier_alignments = get_frontier_alignments(alignments, partial(get_alignment_acc, g1_to_g2_ort=g1_to_g2_ort, adj_set1=adj_set1, adj_set2=adj_set2))
size_acc_points = []

for alignment, size, acc in frontier_alignments:
    size_acc_points.append((size, acc))

print('\n'.join(f'{size} {nc}' for size, nc in size_acc_points))
