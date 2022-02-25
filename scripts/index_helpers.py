#!/bin/python3
from collections import defaultdict
from general_helpers import *

# helps with file paths of cached blant output
PLANT_DIR = '/home/wangph1/plant'
CACHE_BASE_DIR = f'{PLANT_DIR}/data/seeding_cached_data'

class Index(defaultdict):
    def __init__(self):
        defaultdict.__init__(self, list)

    def add_entry(self, entry):
        self[entry.get_graphlet_id()].append(entry)


class IndexEntry:
    def __init__(self, entry_str):
        splitted_str = entry_str.split(' ')
        self._graphlet_id = int(splitted_str[0])
        self._node_arr = splitted_str[1:]
        self._index_of = dict()

        for i, node in enumerate(self._node_arr):
            self._index_of[node] = i

        self._node_set = set(splitted_str[1:])

    def get_graphlet_id(self):
        return self._graphlet_id

    def get_node_arr(self):
        return self._node_arr

    def node_in(self, node):
        return node in self._node_set

    def index_of(self, node):
        if node in self._index_of:
            return self._index_of[node]
        else:
            return -1

    def get_num_matching(self, other_index):
        num_matching = 0

        for node in self._node_arr:
            if node in other_index._node_set:
                num_matching += 1

        return num_matching

    def get_matching_list(self, other_index):
        matching_list = []

        for i, node in enumerate(self._node_arr):
            if node in other_index._node_set:
                matching_list.append(i)

        return matching_list

    def __str__(self):
        return ' '.join(self._node_arr)

    def __len__(self):
        return len(self._node_arr)


def get_index_path(species, percent=0, orbit=0):
    if 'syeast' in species:
        lDEG = 3
    else:
        lDEG = 2

    return f'{CACHE_BASE_DIR}/blant_out/p{percent}-o{orbit}-{species}-lDEG{lDEG}.out'

def get_notopedge_index_path(species, percent=0, orbit=0, lDEG=2):
    return f'{CACHE_BASE_DIR}/special_blant_out/p{percent}-o{orbit}-{species}-lDEG{lDEG}-notopedge.out'

def read_in_index(index_path, k):
    with open(index_path, 'r') as index_file:
        index = Index()

        for curr_entry_str in index_file:
            curr_entry_str = curr_entry_str.strip()
            assert len(curr_entry_str.split(' ')) == k + 1, f'the line {curr_index_str} is not of size k{k}'
            curr_entry = IndexEntry(curr_entry_str)
            index.add_entry(curr_entry)

        return index

if __name__ == '__main__':
    index = read_in_index(get_index_path('mouse'), 8)
    assert_with_prints(len(index), 564, 'len(index)')
