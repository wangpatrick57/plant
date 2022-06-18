#!/pkg/python/3.7.4/bin/python3
from seeding_algorithm_core import *
from node_pair_extraction_helpers import *
from index_helpers import *
from odv_helpers import *
from ortholog_helpers import *
from patch_helpers import *
from validation_helpers import *
from graph_helpers import *

# this file runs the entire algorithm from start to finish, hiding all the internal detailns
def full_get_combined_seeds(k, species1, species2, orbits, max_indices, sims_threshold, print_progress=False):
    all_seeds_lists = []

    for orbit in orbits:
        s1_index_path = get_index_path(species1, orbit=orbit)
        s2_index_path = get_index_path(species2, orbit=orbit)

        if not (validate_index_file(s1_index_path, k) and validate_index_file(s2_index_path, k)):
            print('skipped {species1}-{species2} o{orbit}')
            continue

        all_seeds_list = find_seeds(read_in_index(s1_index_path, k), read_in_index(s2_index_path, k), ODVDirectory(get_odv_path(species1)), ODVDirectory(get_odv_path(species2)), SeedingAlgorithmSettings(max_indices=max_indices, sims_threshold=sims_threshold), print_progress=print_progress)
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
        all_seeds_list = find_seeds(s1_index, s2_index, ODVDirectory(get_odv_path(species1)), ODVDirectory(get_odv_path(species2)), SeedingAlgorithmSettings(max_indices=max_indices, sims_threshold=sims_threshold), print_progress=print_progress)
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

def get_node_coverage(all_seeds):
    nodes = set()

    for _, align1, align2 in all_seeds:
        for node in align1:
            nodes.add(node)

        for node in align2:
            nodes.add(node)

    return len(nodes)

def get_gtag_run_info(gtag1, gtag2, s1_alph=True, s2_alph=True, algo=None, lDEG=2):
    s1_index_path = get_index_path(gtag1, alph=s1_alph, algo=algo, lDEG=lDEG)
    s2_index_path = get_index_path(gtag2, alph=s2_alph, algo=algo, lDEG=lDEG)
    s1_graph_path = get_graph_path(gtag1)
    s2_graph_path = get_graph_path(gtag2)
    s1_to_s2_orthologs = get_g1_to_g2_orthologs(gtag1, gtag2)
    return (s1_index_path, s1_graph_path, s2_index_path, s2_graph_path, s1_to_s2_orthologs)

def get_alphrev_gtag_run_infos(gtag1, gtag2, algo=None):
    infos = []
    
    for s1_alph in [True, False]:
        for s2_alph in [True, False]:
            infos.append(get_gtag_run_info(gtag1, gtag2, s1_alph=s1_alph, s2_alph=s2_alph), algo=algo)

    return infos

def get_alphrev_strs():
    strs = []
    
    for s1_alph in [True, False]:
        for s2_alph in [True, False]:
            str_tup = ('alph' if s1_alph else 'rev', 'alph' if s2_alph else 'rev')
            strs.append(''.join(str_tup))

    return strs

def investigate_alphrev_effect(gtag1, gtag2):
    for alphrev_str, run_info in zip(get_alphrev_strs(), get_alphrev_gtag_run_infos(gtag1, gtag2)):
        seeds, seed_metrics, extr_metrics = low_param_one_run(*run_info)
        print(f'{gtag1}-{gtag2} ({alphrev_str}): {len(seeds)} {seed_metrics} {extr_metrics}')

def results_with_alphrev(gtag1, gtag2):
    pass

# low param means T=0, M=1, p=0, o=0 with two index and graph files
def low_param_one_run(s1_index_path, s1_graph_path, s2_index_path, s2_graph_path, s1_to_s2_orthologs, prox=3, target_num_matching=4):
    k = 8
    s1_index = get_patched_index(k, s1_index_path, s1_graph_path, prox=prox, target_num_matching=target_num_matching)
    s2_index = get_patched_index(k, s2_index_path, s2_graph_path, prox=prox, target_num_matching=target_num_matching)

    # TODO: fix odv stuff
    all_seeds = find_seeds(s1_index, s2_index, ODVDirectory(get_odv_path('syeast0', 5)), ODVDirectory(get_odv_path('syeast0', 5)), SeedingAlgorithmSettings(max_indices=1, sims_threshold=0), print_progress=False)
    avg_nc = get_avg_node_correctness(all_seeds, s1_to_s2_orthologs)
    node_cov = get_node_coverage(all_seeds)
    perf_seed_vol = len(get_orthoseeds_list(all_seeds, s1_to_s2_orthologs))
    seed_metrics = (avg_nc, node_cov, perf_seed_vol)

    all_node_pairs = extract_node_pairs(all_seeds)
    extr_vol = len(all_node_pairs)
    extr_nc = 0 if extr_vol == 0 else len(get_orthopairs_list(all_node_pairs, s1_to_s2_orthologs)) / extr_vol
    extr_metrics = (extr_vol, extr_nc)

    return (all_seeds, seed_metrics, extr_metrics)

def seed_to_str(seed):
    gid, glet1, glet2 = seed
    return '\t'.join([gid, ','.join(glet1), ','.join(glet2)])

def seeds_to_str(seeds):
    return '\n'.join([seed_to_str(seed) for seed in seeds])

if __name__ == '__main__':
    from full_report_helpers import gen_all_indexes

    gtag1 = sys.argv[1]
    gtag2 = sys.argv[2]
    algo = 'bno'
    lDEG = 2
    gtag1, gtag2 = order_gtags(gtag1, gtag2)
    gen_all_indexes([gtag1, gtag2], algo=algo, lDEG=lDEG)
    seeds, seed_metrics, extr_metrics = low_param_one_run(*get_gtag_run_info(gtag1, gtag2, s1_alph=True, s2_alph=True, algo=algo, lDEG=lDEG))
    print(len(seeds), seed_metrics, extr_metrics)
    write_to_file(seeds_to_str(seeds), f'{gtag1}-{gtag2}-seeds.txt')


