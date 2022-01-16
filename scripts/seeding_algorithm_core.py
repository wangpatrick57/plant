from collections import defaultdict
from odv_helpers import *

class SeedingAlgorithmSettings:
    def __init__(self, max_indices=15, sims_threshold=0.79, speedup=1):
        self.max_indices = max_indices
        self.sims_threshold = sims_threshold
        self.speedup = speedup

# takes in necessary inputs and settings and returns a list of all found seeds
def find_seeds(k, species1, species2, s1_index_path, s2_index_path, s1_odv_path, s2_odv_path, settings, print_progress=False):
    s1_odv_dir = ODVDirectory(s1_odv_path)
    s2_odv_dir = ODVDirectory(s2_odv_path)
    s1_indexed_indices = get_indexed_indices(s1_index_path, k)
    s2_indexed_indices = get_indexed_indices(s2_index_path, k)
    total_pairs_to_process = estimate_total_pairs_to_process(s1_indexed_indices, s2_indexed_indices, settings)
    all_seeds_list = []
    percent_printed = 0
    candidate_seeds_processed = 0 # this won't be equal to len(all_seeds_list) because we don't add all candidate seeds

    for graphlet_id, s1_graphlet_indices in s1_indexed_indices.items():
        if graphlet_id not in s2_indexed_indices:
            continue

        s2_graphlet_indices = s2_indexed_indices[graphlet_id]

        if len(s1_graphlet_indices) > settings.max_indices:
            continue

        if len(s2_graphlet_indices) > settings.max_indices:
            continue

        for i in range(0, len(s1_graphlet_indices), settings.speedup):
            s1_index = s1_graphlet_indices[i]

            for j in range(0, len(s2_graphlet_indices), settings.speedup):
                s2_index = s2_graphlet_indices[j]
                missing_nodes = 0

                # determine if we want to make it a seed
                if should_be_seed(s1_index, s2_index, s1_odv_dir, s2_odv_dir, settings.sims_threshold):
                    all_seeds_list.append((graphlet_id, s1_index, s2_index))

                candidate_seeds_processed += 1

                # print
                if print_progress:
                    if candidate_seeds_processed / total_pairs_to_process * 100 > percent_printed:
                        print(f'{percent_printed}% done', file=sys.stderr)
                        percent_printed += 1
        
    return all_seeds_list


# yes these are two different meanings of index
def get_indexed_indices(index_path, k):
    with open(index_path, 'r') as index_file:
        indexed_indices = defaultdict(list)

        for i, line in enumerate(index_file):
            line_split = line.strip().split()
            assert len(line_split) == k + 1, f'{i}: {line.strip()}, files: {index_file.name} and {s2_index_file.name}'
            graphlet_id = int(line_split[0])
            index = line_split[1:]
            indexed_indices[graphlet_id].append(index)
        
        return indexed_indices

def estimate_total_pairs_to_process(s1_indexed_indices, s2_indexed_indices, settings):
    total_graphlet_pairs = 0

    for graphlet_id, s1_graphlet_indices in s1_indexed_indices.items():
        if graphlet_id in s2_indexed_indices:
            s2_graphlet_indices = s2_indexed_indices[graphlet_id]

            if len(s1_graphlet_indices) <= settings.max_indices and len(s2_graphlet_indices) <= settings.max_indices:
                total_graphlet_pairs += len(s1_graphlet_indices) * len(s2_graphlet_indices)

    total_pairs_to_process = int(total_graphlet_pairs / (settings.speedup ** 2))
    return total_pairs_to_process

def should_be_seed(s1_index, s2_index, s1_odv_dir, s2_odv_dir, threshold):
    sims = []

    for s1_node, s2_node in zip(s1_index, s2_index):
        s1_odv = s1_odv_dir.get_odv(s1_node)
        s2_odv = s2_odv_dir.get_odv(s2_node)
        sims.append(s1_odv.get_similarity(s2_odv))

    return mean(sims) >= threshold
