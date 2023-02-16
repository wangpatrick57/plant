#!/pkg/python/3.7.4/bin/python3
from all_helpers import *
from run_sag import get_sag_alignment_path
import sys

if __name__ == '__main__':
    for gtag1, gtag2 in get_iid_mammal_pairs():
        adj_set1 = read_in_adj_set(get_graph_path(gtag1))
        adj_set2 = read_in_adj_set(get_graph_path(gtag2))
        g1_to_g2_ort = get_g1_to_g2_orthologs(gtag1, gtag2)
        sag_alignment_path = get_sag_alignment_path(gtag1, gtag2, auto_k=(10000, 0.01))
        sag_alignment = read_in_alignment(sag_alignment_path, adj_set1, adj_set2)
        cytomcs_alignment_path = get_cytomcs_alignment_path(gtag1, gtag2, perturbation=0, max_num_steps=1)
        cytomcs_alignment = read_in_cytomcs_alignment(cytomcs_alignment_path, adj_set1, adj_set2)

        sag_orts = set(get_alignment_orthologs(sag_alignment, g1_to_g2_ort, adj_set1, adj_set2))
        cytomcs_orts = set(get_alignment_orthologs(cytomcs_alignment, g1_to_g2_ort, adj_set1, adj_set2))
        print(f'For {gtag1}-{gtag2}, SAG found {len(sag_orts)} orthologs in {len(sag_alignment)} pairs, of which {len(sag_orts.intersection(cytomcs_orts))} are present in the {len(cytomcs_orts)} orthologs that CytoMCS found')
