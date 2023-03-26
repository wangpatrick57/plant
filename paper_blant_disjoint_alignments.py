#!/pkg/python/3.7.4/bin/python3
from all_helpers import *
import sys
import os

gtag1 = 'cat'
gtag2 = 'cow'
adj_set1 = read_in_adj_set(get_graph_path(gtag1))
adj_set2 = read_in_adj_set(get_graph_path(gtag2))
g1_to_g2_ort = get_g1_to_g2_orthologs(gtag1, gtag2)
seeds, _, _ = simplified_run_with_metrics(gtag1, gtag2, algo='stairs')
tfp_alignments = get_topofunc_perfect_seeds(seeds, g1_to_g2_ort, adj_set1, adj_set2)
tfp_disjoint_alignments = get_disjoint_alignments(tfp_alignments)
print(distr_to_str(get_alignments_deg_distr(tfp_alignments, adj_set1, True), 'seed node degree'))
print(f'{len(tfp_alignments)} tfp seeds out of {len(seeds)} seeds')
print(f'{len(tfp_disjoint_alignments)} tfp disjoint seeds out of {len(tfp_alignments)} tfp seeds')
