#!/bin/python3
from collections import defaultdict

class SeedingAlgorithmSettings:
    def __init__(self, max_indices=1, sims_threshold=0, speedup=1):
        self.max_indices = max_indices
        self.sims_threshold = sims_threshold
        self.speedup = speedup
        
# takes in necessary inputs and settings and returns a list of all found seeds
def find_seeds(g1_index, g2_index, settings=SeedingAlgorithmSettings(), g1_odv_dir=None, g2_odv_dir=None, print_progress=False):
    total_pairs_to_process = estimate_total_pairs_to_process(g1_index, g2_index, settings)
    all_seeds_list = []
    percent_printed = 0
    candidate_seeds_processed = 0 # this won't be equal to len(all_seeds_list) because we don't add all candidate seeds

    for graphlet_id, g1_gid_entries in g1_index.items():
        if graphlet_id not in g2_index:
            continue

        g2_gid_entries = g2_index[graphlet_id]

        if len(g1_gid_entries) > settings.max_indices:
            continue

        if len(g2_gid_entries) > settings.max_indices:
            continue

        for i in range(0, len(g1_gid_entries), settings.speedup):
            g1_entry_nodes = g1_gid_entries[i].get_node_arr()

            for j in range(0, len(g2_gid_entries), settings.speedup):
                g2_entry_nodes = g2_gid_entries[j].get_node_arr()
                missing_nodes = 0

                # determine if we want to make it a seed
                if should_be_seed(g1_entry_nodes, g2_entry_nodes, g1_odv_dir, g2_odv_dir, settings.sims_threshold):
                    all_seeds_list.append((graphlet_id, tuple(g1_entry_nodes), tuple(g2_entry_nodes)))

                candidate_seeds_processed += 1

                # print
                if print_progress:
                    if candidate_seeds_processed / total_pairs_to_process * 100 > percent_printed:
                        print(f'{percent_printed}% done', file=sys.stderr)
                        percent_printed += 1

    return clean_seeds(all_seeds_list)

def clean_seeds(seeds):
    return list(set(seeds))

def get_combined_seeds_list(seed_lists):
    final_set = set()

    for seed_list in seed_lists:
        for seed in seed_list:
            final_set.add(seed)

    return list(final_set)

def estimate_total_pairs_to_process(g1_index, g2_index, settings):
    total_graphlet_pairs = 0

    for graphlet_id, g1_gid_entries in g1_index.items():
        if graphlet_id in g2_index:
            g2_gid_entries = g2_index[graphlet_id]

            if len(g1_gid_entries) <= settings.max_indices and len(g2_gid_entries) <= settings.max_indices:
                total_graphlet_pairs += len(g1_gid_entries) * len(g2_gid_entries)

    total_pairs_to_process = int(total_graphlet_pairs / (settings.speedup ** 2))
    return total_pairs_to_process

def should_be_seed(g1_entry_nodes, g2_entry_nodes, g1_odv_dir, g2_odv_dir, threshold):
    # speedup for a special case
    if threshold == 0:
        return True

    sims = []

    for g1_node, g2_node in zip(g1_entry_nodes, g2_entry_nodes):
        g1_odv = g1_odv_dir.get_odv(g1_node)
        g2_odv = g2_odv_dir.get_odv(g2_node)
        sims.append(g1_odv.get_similarity(g2_odv))

    return mean(sims) >= threshold

if __name__ == '__main__':
    from index_helpers import get_index_path
    from graph_helpers import get_graph_path
    from patch_helpers import get_patched_index
    from odv_helpers import ODVDirectory, get_odv_path, two_gtags_to_k
    
    gtag1 = 'mouse'
    gtag2 = 'rat'
    k = 8
    g1_index_path = get_index_path(gtag1)
    g2_index_path = get_index_path(gtag2)
    g1_graph_path = get_graph_path(gtag1)
    g2_graph_path = get_graph_path(gtag2)
    g1_index = get_patched_index(k, g1_index_path, g1_graph_path, prox=1, target_num_matching=1)
    g2_index = get_patched_index(k, g2_index_path, g2_graph_path, prox=1, target_num_matching=1)
    g1_odv_dir = ODVDirectory(get_odv_path(gtag1, two_gtags_to_k(gtag1, gtag2)))
    g2_odv_dir = ODVDirectory(get_odv_path(gtag2, two_gtags_to_k(gtag1, gtag2)))
    seeds = find_seeds(g1_index, g2_index, settings=SeedingAlgorithmSettings(max_indices=3), g1_odv_dir=g1_odv_dir, g2_odv_dir=g2_odv_dir)
    print(len(seeds))
