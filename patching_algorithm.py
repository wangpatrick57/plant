import sys
import json
import re
import random
from graph_helpers import *
from ortholog_helpers import *
from collections import defaultdict

# command line input
times_called = 0

k = int(sys.argv[1])
species1 = sys.argv[2]
species2 = sys.argv[3]
s1_index_file = open(sys.argv[4], 'r')
s2_index_file = open(sys.argv[5], 'r')
max_indices = int(sys.argv[6])
NUM_MATCHING_NODES = int(sys.argv[7]) if len(sys.argv) >= 8 else k - 2 # negative for <=, positive for ==
PATCH_PROX_INC = int(sys.argv[8]) if len(sys.argv) >= 9 else 1
DEBUG = bool(eval(sys.argv[9])) if len(sys.argv) >= 10 else True

# constants
MISSING_ALLOWED = 0

# setup
def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, file = sys.stderr, **kwargs)

s1_graph_file = open(get_graph_fname_from_species(species1), 'r')
s2_graph_file = open(get_graph_fname_from_species(species2), 'r')

# main code



class CanonicalIndex:
    def __init__(self, node_arr):
        self._node_arr = node_arr

    def get_node_arr(self):
        return self._node_arr


class PatchedIndex:
    def __init__(self, index1, index2, adj_set):
        # left is min right is max
        if index1.get_graphlet_id() <= index2.get_graphlet_id():
            left_index = index1
            right_index = index2
        else:
            left_index = index2
            right_index = index1

        self._left_connectors = left_index.get_matching_list(right_index) # returns matching nodes in left's array poses
        self._right_connectors = right_index.get_matching_list(left_index) # returns matching nodes in right's array poses
        self._num_matching = len(self._left_connectors)

        # node order in _patched_node_arr [nonmatching nodes of left_index in order] + [matching nodes in left_index order] + [nonmatching nodes of right_index in order]
        # this is the canonical ordering, assuming both graphlets are multiplicity 1. that means, when checking if the seed is a perfect ortholog match, we will make sure that all nodes in one patched index's _patched_node_arr are orthologs with the node in the same position in the other patched index's _patched_node_arr
        self._patched_node_arr = []
        self._matching_poses = [] # stores (g1_pos, g2_pos) of matching nodes
        matching_left_poses = set()
        matching_right_poses = set()

        for i, node in enumerate(left_index.get_node_arr()):
            if not right_index.node_in(node):
                self._patched_node_arr.append(node)

        for i, node in enumerate(left_index.get_node_arr()):
            if right_index.node_in(node):
                self._patched_node_arr.append(node)

                assert right_index.index_of(node) != -1

                self._matching_poses.append((i, right_index.index_of(node)))
                matching_left_poses.add(i)
                matching_right_poses.add(right_index.index_of(node))

        for i, node in enumerate(right_index.get_node_arr()):
            if not left_index.node_in(node):
                self._patched_node_arr.append(node)

        # create extra_edges
        self._extra_edges = dict()

        non_matching_left_poses = [i for i in range(len(left_index)) if i not in matching_left_poses]
        non_matching_right_poses = [i for i in range(len(right_index)) if i not in matching_right_poses]
        
        assert len(right_index) == len(left_index)
        assert len(non_matching_left_poses) == len(non_matching_right_poses) == len(right_index) - self._num_matching

        for left_pos in non_matching_left_poses:
            for right_pos in non_matching_right_poses:
                if left_index.get_node_arr()[left_pos] in adj_set[right_index.get_node_arr()[right_pos]]:
                    if left_pos not in self._extra_edges:
                        self._extra_edges[left_pos] = []

                    self._extra_edges[left_pos].append(right_pos)

        extra_edges_str = '-'.join([f'{key}:' + f'{",".join(str(pos) for pos in value)}' for key, value in sorted(list(self._extra_edges.items()))])
        matching_poses_str = ','.join([f'{g1_pos}:{g2_pos}' for g1_pos, g2_pos in self._matching_poses])
        self._key = f'{left_index.get_graphlet_id()}-{right_index.get_graphlet_id()};{matching_poses_str};{extra_edges_str}'

    def get_node_arr(self):
        return self._patched_node_arr
                    
    def __str__(self):
        return self._key

def get_matching_poses_adj_list(index_list):
    matching_poses_adj_list = []
    total_to_check = len(index_list)
    num_checked = 0

    for i in range(0, len(index_list)):
        matching_poses_adj_list.append([])
        outer_index = index_list[i]

        for j in range(i + PATCH_PROX_INC, i + PATCH_PROX_INC + 1):
            if j >= len(index_list):
                continue

            inner_index = index_list[j]
            num_matching = outer_index.get_num_matching(inner_index)

            if NUM_MATCHING_NODES < 0:
                do_append = num_matching >= -1 * NUM_MATCHING_NODES
            else:
                do_append = num_matching == NUM_MATCHING_NODES

            if do_append:
                matching_poses_adj_list[i].append(j)

            num_checked += 1

    num_total_matches = sum(len(matching_list) for matching_list in matching_poses_adj_list)
    debug_print(f'for {NUM_MATCHING_NODES} matching nodes, there are {num_total_matches} out of {num_checked} matches, or {num_total_matches * 100 / num_checked}%')
    return matching_poses_adj_list

def sparsegraph_arr2str(arr):
    return f'{",".join(str(elem) for elem in arr)}'

def node_arr_to_sparsegraph(node_arr, adj_set):
    nv = len(node_arr)
    nde = 0
    d = [0] * nv
    v = [0] * nv
    e = []

    for i in range(len(node_arr)):
        base_node = node_arr[i]

        if i != len(node_arr) - 1:
            v[i + 1] = v[i]

        for j in range(len(node_arr)):
            if i == j:
                continue

            compare_node = node_arr[j]

            if compare_node in adj_set[base_node]:
                assert base_node in adj_set[compare_node]
                e.append(j)
                d[i] += 1

                if i != len(node_arr) - 1:
                    v[i + 1] += 1

                nde += 1
            else:
                assert base_node not in adj_set[compare_node]

    return f'{nv};{nde};{sparsegraph_arr2str(v)};{sparsegraph_arr2str(d)};{sparsegraph_arr2str(e)}'

def get_patched_indexes(matching_poses_adj_list, index_list, adj_set):
    patched_indexes = dict()

    for i, matching_list in enumerate(matching_poses_adj_list):
        for j in matching_list:
            patched_index = PatchedIndex(index_list[i], index_list[j], adj_set)
            patched_index_key = str(patched_index)
            
            if patched_index_key not in patched_indexes:
                patched_indexes[patched_index_key] = []

            patched_indexes[patched_index_key].append(patched_index)

    return patched_indexes

def get_core_to_core(adj_set):
    core_to_core = dict()

    for node in adj_set:
        if node[0:4] == 'core':
            core_to_core[node] = node

    return core_to_core

def get_num_missing(base_index, comp_index_list, base_to_comp_list):
    assert len(comp_index_list) == len(base_to_comp_list)
    missing_nodes_list = [0] * len(comp_index_list)

    for m in range(len(base_index)):
        base_node = base_index[m]

        for i in range(len(comp_index_list)):
            comp_node = comp_index_list[i][m]
            base_to_comp = base_to_comp_list[i]

            if base_node not in base_to_comp or base_to_comp[base_node] != comp_node:
                missing_nodes_list[i] += 1

    return missing_nodes_list

def get_orthologs_list(base_indexes, comp_indexes_list, base_to_comp_list, adj_set_list):
    orthologs_list = []
    full_match_distr = defaultdict(int)
    pairs_processed = 0
    percent_to_print = 0
    pairs_to_process = 0
    debug_print('about to calculate pairs_to_process')

    for patched_id in base_indexes:
        for comp_indexes in comp_indexes_list:
            if patched_id in comp_indexes and len(base_indexes[patched_id]) <= max_indices and len(comp_indexes[patched_id]) <= max_indices:
                pairs_to_process += len(base_indexes[patched_id]) * len(comp_indexes[patched_id])

    comp_patched_indexes_list = [None] * len(comp_indexes_list)

    debug_print('done calculating pairs_to_process')

    for patched_id, base_patched_indexes in base_indexes.items():
        do_continue = False

        for i, comp_indexes in enumerate(comp_indexes_list):
            if patched_id in comp_indexes:
                comp_patched_indexes_list[i] = comp_indexes[patched_id]
            else:
                do_continue = True

        if do_continue:
            continue

        if len(base_patched_indexes) > max_indices or any([len(comp_patched_indexes) > max_indices for comp_patched_indexes in comp_patched_indexes_list]):
            continue

        for base_index in base_patched_indexes:
            base_index = base_index.get_node_arr()

            for comp_index in comp_index_list[0]:
                comp_index = comp_index.get_node_arr()
                assert len(base_index) > k and len(base_index) == len(comp_index), f'lengths not good'
                # NOTE: wrote up to here, next, need to check if it's an ortholog match and if it is, create a new_seed.
                # next, fix this so we take in comp_index instead of comp_index_list

        is_ortho = check_if_ortholog(base_index, comp_index_list, base_to_comp_list)
        new_seed = [patched_id, base_index]
        new_seed.extend(comp_index_list)
        orthologs_list.append((new_seed, is_ortho))
        pairs_processed += 1

        if pairs_processed * 100 / pairs_to_process > percent_to_print:
            debug_print(f'{pairs_processed * 100 / pairs_to_process}% done')
            percent_to_print += 1

    num_orthologs = sum(1 if is_ortho else 0 for _, is_ortho in orthologs_list)

    if pairs_processed == 0:
        ortholog_percent = -1
    else:
        ortholog_percent = num_orthologs * 100 / pairs_processed

    debug_print(f'on settings NUM_MATCHING_NODES={NUM_MATCHING_NODES} PATCH_PROX_INC={PATCH_PROX_INC}, there are {num_orthologs} {MISSING_ALLOWED}|miss orthologs out of {pairs_processed} processed patched pairs, representing {ortholog_percent}%')
    return orthologs_list


def seed_to_str(patch_id, index1, index2):
    return f'{patch_id} {",".join(index1)} {",".join(index2)}'

def print_sorted_sparsegraphs(dict_list, adj_set_list): # sorted by key
    key_to_sparsegraph = dict()
    
    for this_dict, this_adj_set in zip(dict_list, adj_set_list):
        for key in this_dict:
            key_to_sparsegraph[key] = node_arr_to_sparsegraph(this_dict[key][0].get_node_arr(), this_adj_set)

    for key in sorted(key_to_sparsegraph.keys()):
        print(key_to_sparsegraph[key])

def main():
    debug_print('algorithm starting')

    # read in index files
    s1_adj_set = read_adj_set(s1_graph_file)
    s1_index_list = read_index_file(s1_index_file)
    s2_adj_set = read_adj_set(s2_graph_file)
    s2_index_list = read_index_file(s2_index_file)

    debug_print('done reading files')

    # find pairs with enough nodes matching
    s1_matching_poses_adj_list = get_matching_poses_adj_list(s1_index_list)
    s2_matching_poses_adj_list = get_matching_poses_adj_list(s2_index_list)

    # patch indexes
    s1_patched_indexes = get_patched_indexes(s1_matching_poses_adj_list, s1_index_list, s1_adj_set)
    s2_patched_indexes = get_patched_indexes(s2_matching_poses_adj_list, s2_index_list, s2_adj_set)

    debug_print('done patching indexes')

    ## CHANGE MODE
    # print_sorted_sparsegraphs([s1_patched_indexes, s2_patched_indexes], [s1_adj_set, s2_adj_set])

    # calculate ortholog percentage
    s1_to_s2 = get_s1_to_s2_orthologs(species1, species2)
    orthologs_list = get_orthologs_list(s1_patched_indexes, [s2_patched_indexes], [s1_to_s2], [s1_adj_set, s2_adj_set])
    
    for seed, is_ortho in orthologs_list:
        if is_ortho:
            print(seed_to_str(*seed))


if __name__ == '__main__':
    main()
