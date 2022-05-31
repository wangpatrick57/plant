#!/pkg/python/3.7.4/bin/python3
import sys
import math
import heapq
from statistics import mean
from graph_helpers import *

def get_odv_file_path(species):
    return f'{get_graph_path(species)}.orca4'

class ODVDirectory:
    # file format: every line has node name, followed by orbit counts, separated by spaces
    # NODENAME 23 1 250 37 4 0 ...
    def __init__(self, fname):
        self._directory = dict()

        for line in open(fname, 'r'):
            line_split = line.strip().split()
            node = line_split[0]
            odv_list = [int(s) for s in line_split[1:]]
            odv = ODV(odv_list)
            self._directory[node] = odv

    def get_odv(self, node):
        return self._directory[node]

    def get_nodes(self):
        return self._directory.keys()

    def __str__(self):
        return '\n'.join([f'{node}: {odv}' for node, odv in self._directory.items()])


class ODV:
    WEIGHTS = [1] * 4
    WEIGHT_SUM = sum(WEIGHTS)

    def __init__(self, odv_list):
        self._odv_list = odv_list

    def get_similarity(self, other):
        assert len(self._odv_list) == len(other._odv_list) == len(ODV.WEIGHTS)
        distance_sum = sum([self._get_single_orbit_similarity(m1, m2, i) for i, (m1, m2) in enumerate(zip(self._odv_list, other._odv_list))])
        weight_sum = ODV.WEIGHT_SUM
        return 1 - distance_sum / weight_sum

    def get_mean_similarity(self, other):
        return mean([self._get_single_orbit_mean_similarity(m1, m2) for m1, m2 in zip(self._odv_list, other._odv_list)])

    def get_odv_val(self, num):
        return self._odv_list[num]

    def __str__(self):
        return ' '.join([str(n) for n in self._odv_list])

    @staticmethod
    def _get_single_orbit_mean_similarity(m1, m2):
        return 1 if m1 == m2 == 0 else min(m1, m2) / max(m1, m2)

    @staticmethod
    def _get_single_orbit_similarity(m1, m2, i):
        # the base of the log doesn't matter
        top_inner = math.log(m1 + 1) - math.log(m2 + 1)
        bot = math.log(max(m1, m2) + 2)
        return abs(top_inner) / bot

def get_odv_orthologs(nodes1, nodes2, odv_dir1, odv_dir2, k):
    assert k <= len(nodes1) * len(nodes2)
    top_k = [(-1, '', '')] * k
    heapq.heapify(top_k)

    for node1 in nodes1:
        for node2 in nodes2:
            if odv_dir1 == odv_dir2 == None:
                val = {'a': 1, 'b': 7, 'c': 10, 'd': 2, 'e': 5, 'f': 8}
                sim = 10 - abs(val[node1] - val[node2])
            else:
                odv1 = odv_dir1.get_odv(node)
                odv2 = odv_dir2.get_odv(node)
                sim = odv1.get_similarity(odv2)

            min_node = min(node1, node2)
            max_node = max(node1, node2)
            obj = (sim, min_node, max_node)
            min_top = heapq.heappushpop(top_k, obj)

    return sorted(top_k, reverse=True)

if __name__ == '__main__':
    path1 = get_base_graph_path('test1')
    path2 = get_base_graph_path('test2')
    nodes1 = read_in_nodes(path1)
    nodes2 = read_in_nodes(path2)
    print(get_odv_orthologs(nodes1, nodes2, None, None, 5))
