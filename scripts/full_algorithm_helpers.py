#!/bin/python3
# this file runs the entire algorithm from start to finish, hiding all the internal details
from seeding_algorithm_core import *
from node_pair_extraction_helpers import *
from blant_cache_helpers import *
from odv_helpers import *
from ortholog_helpers import *

def full_get_combined_seeds(k, species1, species2, orbits, max_indices, sims_threshold, print_progress=False):
    all_seeds_lists = []

    for orbit in orbits:
        all_seeds_list = find_seeds(k, species1, species2, get_index_path(species1, orbit=orbit), get_index_path(species2, orbit=orbit), get_odv_file_path(species1), get_odv_file_path(species2), SeedingAlgorithmSettings(max_indices=max_indices, sims_threshold=sims_threshold))
        all_seeds_lists.append(all_seeds_list)

        if print_progress:
            print(f'done with orbit {orbit}')

    return get_combined_seeds_list(all_seeds_lists)

# returns (num_orthopairs, num_all_pairs)
def full_run_algorithm_basic(k, species1, species2, orbits, max_indices, sims_threshold, print_progress=False):
    combined_seeds = full_get_combined_seeds(k, species1, species2, orbits, max_indices, sims_threshold, print_progress=print_progress)
    node_pairs = extract_node_pairs(combined_seeds)
    s1_to_s2_orthologs = get_s1_to_s2_orthologs("mouse", "rat")
    orthopairs_list = get_orthopairs_list(node_pairs, s1_to_s2_orthologs)
    return (orthopairs_list, node_pairs)

# def full_run_algorithm_auto_threshold(k, species1, species2, orbits, max_indices):
