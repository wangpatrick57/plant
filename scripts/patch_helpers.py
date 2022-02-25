#!/bin/python3
from index_helpers import *
from graph_helpers import *
from general_helpers import *

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


def get_matching_poses_list(index_list, prox, target_num_matching):
    matching_poses_list = []
    total_to_check = len(index_list)
    num_checked = 0

    for i in range(0, len(index_list)):
        matching_poses_list.append([])
        outer_index = index_list[i]

        for j in range(i + prox, i + prox + 1):
            if j >= len(index_list):
                continue

            inner_index = index_list[j]
            curr_num_matching = outer_index.get_num_matching(inner_index)

            if target_num_matching < 0:
                do_append = curr_num_matching >= -1 * target_num_matching
            else:
                do_append = curr_num_matching == target_num_matching

            if do_append:
                matching_poses_list[i].append(j)

            num_checked += 1

    return matching_poses_list

def get_patched_indexes(matching_poses_list, index_list, adj_set):
    patched_indexes = dict()

    for i, matching_list in enumerate(matching_poses_list):
        for j in matching_list:
            patched_index = PatchedIndex(index_list[i], index_list[j], adj_set)
            patched_index_key = str(patched_index)
            
            if patched_index_key not in patched_indexes:
                patched_indexes[patched_index_key] = []

            patched_indexes[patched_index_key].append(patched_index)

    return patched_indexes

if __name__ == '__main__':
    index_list = read_in_entry_list(get_index_path('mouse'), 8)
    adj_set = read_in_adj_set(get_graph_path('mouse'))
    patched_indexes = get_patched_indexes(get_matching_poses_list(index_list, 6, 6), index_list, adj_set)
    assert_with_prints(len(patched_indexes), 6833, 'len(patched_indexes)')
