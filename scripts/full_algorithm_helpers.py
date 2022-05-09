#!/pkg/python/3.7.4/bin/python3
# this file runs the entire algorithm from start to finish, hiding all the internal detailns
from seeding_algorithm_core import *
from node_pair_extraction_helpers import *
from index_helpers import *
from odv_helpers import *
from ortholog_helpers import *
from patch_helpers import *
from validation_helpers import *
from graph_helpers import *

def full_get_combined_seeds(k, species1, species2, orbits, max_indices, sims_threshold, print_progress=False):
    all_seeds_lists = []

    for orbit in orbits:
        s1_index_path = get_index_path(species1, orbit=orbit)
        s2_index_path = get_index_path(species2, orbit=orbit)

        if not (validate_index_file(s1_index_path, k) and validate_index_file(s2_index_path, k)):
            print('skipped {species1}-{species2} o{orbit}')
            continue

        all_seeds_list = find_seeds(k, read_in_index(s1_index_path, k), read_in_index(s2_index_path, k), ODVDirectory(get_odv_file_path(species1)), ODVDirectory(get_odv_file_path(species2)), SeedingAlgorithmSettings(max_indices=max_indices, sims_threshold=sims_threshold), print_progress=print_progress)
        all_seeds_lists.append(all_seeds_list)

        if print_progress:
            print(f'done with orbit {orbit}')

    return get_combined_seeds_list(all_seeds_lists)

def full_get_patch_combined_seeds(k, species1, species2, orbits, max_indices, sims_threshold, print_progress=False):
    all_seeds_lists = []

    for orbit in orbits:
        s1_index_path = get_index_path(species1, orbit=orbit)
        s2_index_path = get_index_path(species2, orbit=orbit)

        if not (validate_index_file(s1_index_path, k) and validate_index_file(s2_index_path, k)):
            print('skipped {species1}-{species2} o{orbit}')
            continue

        s1_graph_path = get_graph_path(species1)
        s2_graph_path = get_graph_path(species2)
        s1_index = get_patched_index(k, s1_index_path, s1_graph_path)
        s2_index = get_patched_index(k, s2_index_path, s2_graph_path)
        all_seeds_list = find_seeds(10, s1_index, s2_index, ODVDirectory(get_odv_file_path(species1)), ODVDirectory(get_odv_file_path(species2)), SeedingAlgorithmSettings(max_indices=max_indices, sims_threshold=sims_threshold), print_progress=print_progress)
        all_seeds_lists.append(all_seeds_list)

        if print_progress:
            print(f'done with orbit {orbit}')

    return get_combined_seeds_list(all_seeds_lists)

def full_get_seeds_results(k, species1, species2, orbits, max_indices, sims_threshold, print_progress=False):
    combined_seeds = full_get_combined_seeds(k, species1, species2, orbits, max_indices, sims_threshold, print_progress=print_progress)
    # node_pairs = extract_node_pairs(combined_seeds)
    s1_to_s2_orthologs = get_s1_to_s2_orthologs(species1, species2)
    # orthopairs_list = get_orthopairs_list(node_pairs, s1_to_s2_orthologs)
    orthoseeds = get_orthoseeds_list(combined_seeds, s1_to_s2_orthologs)
    return (orthoseeds, combined_seeds)

def full_get_pairs_results(k, species1, species2, orbits, max_indices, sims_threshold, print_progress=False):
    combined_seeds = full_get_combined_seeds(k, species1, species2, orbits, max_indices, sims_threshold, print_progress=print_progress)
    node_pairs = extract_node_pairs(combined_seeds)
    s1_to_s2_orthologs = get_s1_to_s2_orthologs(species1, species2)
    orthopairs = get_orthopairs_list(node_pairs, s1_to_s2_orthologs)
    return (orthopairs, node_pairs)

def full_get_patch_pairs_results(k, species1, species2, orbits, max_indices, sims_threshold, print_progress=False):
    combined_seeds = full_get_patch_combined_seeds(k, species1, species2, orbits, max_indices, sims_threshold, print_progress=print_progress)
    node_pairs = extract_node_pairs(combined_seeds)
    s1_to_s2_orthologs = get_s1_to_s2_orthologs(species1, species2)
    orthopairs = get_orthopairs_list(node_pairs, s1_to_s2_orthologs)
    return (orthopairs, node_pairs)

# low param means T=0, M=1, p=0, o=0 with two index and graph files
def low_param_full_patch_results(s1_index_path, s1_graph_path, s2_index_path, s2_graph_path, s1_to_s2_orthologs, prox=6, target_num_matching=6):
    k = 8
    s1_index = get_patched_index(k, s1_index_path, s1_graph_path, prox=prox, target_num_matching=target_num_matching)
    s2_index = get_patched_index(k, s2_index_path, s2_graph_path, prox=prox, target_num_matching=target_num_matching)
    # TODO: fix odv stuff
    all_seeds = find_seeds(10, s1_index, s2_index, ODVDirectory(get_odv_file_path('mouse')), ODVDirectory(get_odv_file_path('rat')), SeedingAlgorithmSettings(max_indices=1, sims_threshold=0), print_progress=False)
    node_pairs = extract_node_pairs(all_seeds)
    orthopairs = get_orthopairs_list(node_pairs, s1_to_s2_orthologs)
    return (orthopairs, node_pairs)

if __name__ == '__main__':
    s1_index_path = get_index_path('rat')
    s1_graph_path = get_graph_path('rat')
    s2_index_path = get_index_path('mouse')
    s2_graph_path = get_graph_path('mouse')
    s1_to_s2_orthologs = get_s1_to_s2_orthologs('rat', 'mouse')

    orth = []
    total = []

    for target_num_matching in range(6, 8):
        orth.append([])
        total.append([])

        for prox in range(6, 8):
            orthopairs, node_pairs = low_param_full_patch_results(s1_index_path, s1_graph_path, s2_index_path, s2_graph_path, s1_to_s2_orthologs, prox=prox, target_num_matching=target_num_matching)
            orth[-1].append(len(orthopairs))
            total[-1].append(len(node_pairs))
            print(f'done with t{target_num_matching} p{prox}')

    print('orth')
    print('\n'.join(['\t'.join([f'{num}' for num in row]) for row in orth]))
    print()
    print('total')
    print('\n'.join(['\t'.join([f'{num}' for num in row]) for row in total]))
