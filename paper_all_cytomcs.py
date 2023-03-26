#!/bin/python3
from cytomcs_helpers import *

def print_cytomcs_results(pairs, perturbation=DEFAULT_PERTURBATION, max_nonimproving=DEFAULT_MAX_NONIMPROVING, max_num_steps=DEFAULT_MAX_NUM_STEPS, random_seed=None):
    for gtag1, gtag2 in pairs:
        alignment_path = get_cytomcs_alignment_path(gtag1, gtag2, perturbation=perturbation, max_nonimproving=max_nonimproving, max_num_steps=max_num_steps, random_seed=random_seed)

        if os.path.exists(alignment_path):
            adj_set1 = read_in_adj_set(get_graph_path(gtag1))
            adj_set2 = read_in_adj_set(get_graph_path(gtag2))
            g1_to_g2_ort = get_g1_to_g2_orthologs(gtag1, gtag2)
            alignment = read_in_cytomcs_alignment(alignment_path, adj_set1, adj_set2)
            size = len(alignment)
            nc = get_alignment_nc(alignment, g1_to_g2_ort, adj_set1, adj_set2)
            s3 = get_s3(alignment, adj_set1, adj_set2)
            print(f'{gtag1}-{gtag2}', size, nc, size * nc, s3)
        else:
            print(f'{gtag1}-{gtag2} doesn\'t exist')

if __name__ == '__main__':
    pairs = get_iid_mammal_pairs()
    print_cytomcs_results(pairs, max_num_steps=1, perturbation=0)
