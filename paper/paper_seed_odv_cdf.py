#!/bin/python3
import sys
from all_helpers import *

def print_cdf(lst, step_size=0.1):
    sorted_lst = sorted(lst)
    cdf = []
    sep = '\t'
    current = 0
    i = 0

    while current < 1:
        if len(cdf) == 0:
            cdf.append(0)
        else:
            cdf.append(cdf[-1])

        while i < len(lst) and sorted_lst[i] <= current:
            cdf[-1] += 1 / len(lst)
            i += 1
        
        current += step_size
    
    print('\n'.join([f'{step_size * i}{sep}{val}' for i, val in enumerate(cdf)]))

def print_seeds_cdf(gtag1, gtag2, do_patch=True, silent=False):
    seeds, _, _ = simplified_run_with_metrics(gtag1, gtag2, settings=SeedingAlgorithmSettings(max_indices=1, sims_threshold=0), do_patch=do_patch, silent=silent)
    odv_k = two_gtags_to_k(gtag1, gtag2)
    ODV.set_weights_vars(odv_k)
    g1_odv_dir = ODVDirectory(get_odv_path(gtag1, odv_k))
    g2_odv_dir = ODVDirectory(get_odv_path(gtag2, odv_k))
    seed_sim_values = []

    for gid, g1_entry_nodes, g2_entry_nodes in seeds:
        assert(len(g1_entry_nodes) == len(g2_entry_nodes))
        this_seed_sim = sum(g1_odv_dir.get_odv(g1_node).get_similarity(g2_odv_dir.get_odv(g2_node)) for g1_node, g2_node in zip(g1_entry_nodes, g2_entry_nodes)) / len(g1_entry_nodes)
        seed_sim_values.append(this_seed_sim)
    
    print_cdf(seed_sim_values, step_size=0.002)
    
if __name__ == '__main__':
    gtag1 = sys.argv[1]
    gtag2 = sys.argv[2]
    print_seeds_cdf(gtag1, gtag2, do_patch=True)
