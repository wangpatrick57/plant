#!/pkg/python/3.7.4/bin/python3
import sys
import math
import heapq
from collections import defaultdict
from statistics import mean
from bash_helpers import *
from graph_helpers import *

def get_odv_path(gtag, k):
    return get_data_path(f'odv/{gtag}-k{k}.odv')

def gtag_to_k(gtag):
    from graph_helpers import is_syeast
    if is_syeast(gtag):
        return 5
    else:
        return 4

def gtag_to_n(gtag):
    if gtag in {'tester', 'alphabet', 'alpha10'}:
        return 5
    else:
        return 15000

def two_gtags_to_k(gtag1, gtag2):
    assert gtag_to_k(gtag1) == gtag_to_k(gtag2)
    k = gtag_to_k(gtag1)
    return k

def two_gtags_to_n(gtag1, gtag2):
    assert gtag_to_n(gtag1) == gtag_to_n(gtag2)
    n = gtag_to_n(gtag1)
    return n

def num_graphlets(k):
    if k == 5:
        return 30
    elif k == 4:
        return 9
    else:
        return None

def num_orbits(k):
    if k == 5:
        return 73
    elif k == 4:
        return 15
    else:
        return None

def calc_orbit_counts(k):
    USE_CACHE = True

    if USE_CACHE:
        if k == 5:
            return [1, 2, 2, 2, 3, 4, 3, 3, 4, 3, 4, 4, 4, 4, 3, 4, 6, 5, 4, 5, 6, 6, 4, 4, 5, 5, 8, 4, 6, 6, 7, 5, 6, 6, 6, 5, 6, 7, 7, 5, 7, 7, 7, 6, 5, 5, 6, 8, 8, 6, 6, 8, 6, 9, 6, 6, 4, 6, 6, 8, 9, 6, 6, 8, 8, 6, 7, 7, 8, 5, 6, 6, 4]
        elif k == 4:
            return [1, 2, 2, 2, 3, 4, 3, 3, 4, 3, 4, 4, 4, 4, 3]
        else:
            return None
    else:
        orbit_counts = [None] * num_orbits(k)

        for graphlet_num in range(num_graphlets(k)):
            p = run_orca_raw(k, get_base_graph_path(f'graphlets/graphlet{graphlet_num}'))
            orbit_lines = p.stdout.decode().strip().split('\n')[1:]

            for line in orbit_lines:
                splitted = line.split()
                node_name = splitted[0]
                orbit_num = int(node_name[:-1])
                orbits = splitted[1:]

                # we can't just sum all the orbits, we need to count how many are not zero (because if a node has a degree of 5 we only count that once for "an appearance of orbit 0)
                # we include the orbits effect on itself too
                orbit_count = sum([1 if n != '0' else 0 for n in orbits])

                if orbit_counts[orbit_num] == None:
                    orbit_counts[orbit_num] = orbit_count
                else:
                    assert orbit_counts[orbit_num] == orbit_count

        return orbit_counts

def calc_weights(k):
    orbit_counts = calc_orbit_counts(k)
    weights = [1 - math.log(orbit_count) / math.log(num_orbits(k)) for orbit_count in orbit_counts]
    return weights

class ODVDirectory:
    # file format: every line has node name, followed by orbit counts, separated by spaces
    # NODENAME 23 1 250 37 4 0 ...
    def __init__(self, fname):
        self._directory = dict()

        for line in open(fname, 'r'):
            line_split = line.strip().split()
            node = line_split[0]
            odv_list = [int(s) for s in line_split[1:]]
            odv = ODV(node, odv_list)
            self._directory[node] = odv

    def get_odv(self, node):
        return self._directory[node]

    def get_nodes(self):
        return self._directory.keys()

    def __str__(self):
        return '\n'.join([f'{node}: {odv}' for node, odv in self._directory.items()])


class ODV:
    WEIGHTS = []
    WEIGHT_SUM = 0

    @staticmethod
    def set_weights_vars(k):
        ODV.WEIGHTS = calc_weights(k)
        ODV.WEIGHT_SUM = sum(ODV.WEIGHTS) # 45.08670802954777 <- calculated value from .sim file

    def __init__(self, node, odv_list):
        self._node = node
        self._odv_list = odv_list

    def get_similarity(self, other):
        assert len(self._odv_list) == len(other._odv_list) == len(ODV.WEIGHTS), f'self: {len(self._odv_list)}, other: {len(other._odv_list)}, weights: {len(ODV.WEIGHTS)}, self._node: {self._node}, other._node: {other._node}'
        distance_sum = sum([self._get_single_orbit_similarity(m1, m2, i) for i, (m1, m2) in enumerate(zip(self._odv_list, other._odv_list))])
        weight_sum = ODV.WEIGHT_SUM
        return 1 - distance_sum / weight_sum

    def get_inequal_orbits(self, other):
        assert len(self._odv_list) == len(other._odv_list) == len(ODV.WEIGHTS), f'self: {len(self._odv_list)}, other: {len(other._odv_list)}, weights: {len(ODV.WEIGHTS)}'

        inequal_orbits = []

        for i, (o1, o2) in enumerate(zip(self._odv_list, other._odv_list)):
            if o1 != o2:
                inequal_orbits.append(i)

        return inequal_orbits

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
        return ODV.WEIGHTS[i] * abs(top_inner) / bot

def read_in_nodes_wo_deg1(gtag):
    graph_path = get_graph_path(gtag)
    nodes = read_in_nodes(graph_path)
    adj_set = read_in_adj_set(graph_path)
    new_nodes = [node for node in nodes if len(adj_set[node]) > 1]
    return new_nodes

def get_odv_orthologs_lvg_method(gtag1, gtag2, k, n, no1=False):
    if no1:
        nodes1 = read_in_nodes_wo_deg1(gtag1)
        nodes2 = read_in_nodes_wo_deg1(gtag2)
    else:
        nodes1 = list(read_in_nodes(get_graph_path(gtag1)))
        nodes2 = list(read_in_nodes(get_graph_path(gtag2)))

    odv_path1 = get_odv_path(gtag1, k)
    odv_path2 = get_odv_path(gtag2, k)
    odv_dir1 = ODVDirectory(odv_path1)
    odv_dir2 = ODVDirectory(odv_path2)

    assert n <= len(nodes1) * len(nodes2)

    top_n = [(-1, '', '')] * n
    heapq.heapify(top_n)
    tot_nodes = len(nodes1) # approximation for less incrementing
    proc_nodes = 0
    percent_printed = 0
    skip = 1

    for node1 in nodes1:
        for i in range(0, len(nodes2), skip):
            node2 = nodes2[i]
            odv1 = odv_dir1.get_odv(node1)
            odv2 = odv_dir2.get_odv(node2)
            sim = odv1.get_similarity(odv2)
            # don't do min/max node just for sorting purposes, because the nodes come from two different graphs
            # min_node = min(node1, node2) BAD
            # max_node = max(node1, node2) BAD
            obj = (sim, node1, node2)
            min_top = heapq.heappushpop(top_n, obj)
        
        proc_nodes += 1

        if proc_nodes * 1000 / tot_nodes > percent_printed:
            percent_printed += 1
            print(f'{proc_nodes} / {tot_nodes}', file=sys.stderr)

    return sorted(top_n, reverse=True)

def get_odv_orthologs_balanced_method(gtag1, gtag2, k, n):
    pass

def get_odv_orthologs(gtag1, gtag2, k, n):
    return get_odv_orthologs_lvg_method(gtag1, gtag2, k, n, no1=True)

def analyze_mcl_test_data():
    nif1_path = get_data_path('mcl/mcl_test/ppi1.nif')
    nif2_path = get_data_path('mcl/mcl_test/ppi2.nif')
    ort_path = get_data_path('mcl/mcl_test/ppi1-ppi2.ort')
    ppi1_nodes = set()
    ppi2_nodes = set()

    with open(nif1_path, 'r') as nif1:
        for line in nif1:
            node1, node2, _ = line.strip().split('\t')
            ppi1_nodes.add(node1)
            ppi1_nodes.add(node2)

    with open(nif2_path, 'r') as nif2:
        for line in nif2:
            node1, node2, _ = line.strip().split('\t')
            ppi2_nodes.add(node1)
            ppi2_nodes.add(node2)

    ort_ppi1_nodes = set()
    ort_ppi2_nodes = set()

    with open(ort_path, 'r') as ort:
        for line in ort:
            print(line)
            node1, node2, _ = line.strip().split('\t')
            ort_ppi1_nodes.add(node1)
            ort_ppi2_nodes.add(node2)

    print(len(ppi1_nodes), len(ort_ppi1_nodes))
    print(len(ppi2_nodes), len(ort_ppi2_nodes))
    all_nodes = ppi1_nodes.union(ppi2_nodes)
    all_ort_nodes = ort_ppi1_nodes.union(ort_ppi2_nodes)
    print(len(all_nodes), len(all_ort_nodes))

def get_fake_ort_path(base, ext):
    return get_data_path(f'mcl/fake_ort/{base}.{ext}')

def get_odv_ort_path(gtag1, gtag2, k, n):
    return get_fake_ort_path(f'{gtag1}-{gtag2}-k{k}-n{n}-no1', 'ort')

def get_default_odv_ort_path(gtag1, gtag2):
    k = two_gtags_to_k(gtag1, gtag2)
    n = two_gtags_to_n(gtag1, gtag2)
    return get_odv_ort_path(gtag1, gtag2, k, n)

def read_in_odv_orts(path):
    with open(path, 'r') as f:
        lines = f.readlines()
        return [line.split('\t') for line in lines]

def odv_ort_file_to_nodes(path, left):
    from graph_helpers import unmark_node

    with open(path, 'r') as f:
        nodes = []

        for line in f:
            marked_node1, marked_node2, score = line.strip().split('\t')
            node1 = unmark_node(marked_node1)
            node2 = unmark_node(marked_node2)

            if left:
                nodes.append(node1)
            else:
                nodes.append(node2)

        return nodes

def odv_ort_to_nodes(odv_orts, left):
    nodes = list()

    for score, node1, node2 in odv_orts:
        if left:
            nodes.append(node1)
        else:
            nodes.append(node2)

    return nodes

def gen_fake_ort_from_sim(base, k, n):
    sim_path = get_fake_ort_path(base, 'sim')
    ort_path = get_fake_ort_path(f'{base}-{k}', 'ort')
    added_nodes = set()

    with open(sim_path, 'r') as sim_f:
        with open(ort_path, 'w') as ort_f:
            i = 0

            for line in sim_f:
                node1, node2, score = line.split()
                marked_node2 = f'sy05_{node2}'

                if i < n:
                    added_nodes.add(node1)
                    added_nodes.add(node2)
                    ort_f.write('\t'.join([node1, marked_node2, score]) + '\n')
                    i += 1
                else:
                    break

# function I used to validate the sim function based on Hayes' sim files
def validate_sim_function(gtag1, gtag2):
    FACTOR = 1_000_000

    odv_path1 = get_odv_path(gtag1, 5)
    odv_path2 = get_odv_path(gtag2, 5)
    odv_dir1 = ODVDirectory(odv_path1)
    odv_dir2 = ODVDirectory(odv_path2)
    sim_path = get_fake_ort_path(f'{gtag1}-{gtag2}', 'sim')

    tot_diff = 0
    tot_pairs = 0
    num_gt10 = 0

    with open(sim_path, 'r') as sim_file:
        for line in sim_file:
            node1, node2, sim = line.strip().split()
            sim = float(sim)
            sim_non_decimal = int(sim * FACTOR) # cuz the sim_path values are rounded to six
            odv1 = odv_dir1.get_odv(node1)
            odv2 = odv_dir2.get_odv(node2)
            my_sim = odv1.get_similarity(odv2)
            my_sim_non_decimal = int(my_sim * FACTOR)
            tot_diff += abs(sim_non_decimal - my_sim_non_decimal)
            tot_pairs += 1

            if tot_pairs % 5000 == 0:
                print(tot_pairs, '/', 1004 ** 2)

            if tot_pairs > 10000:
                break

    avg_diff = (tot_diff / tot_pairs) / FACTOR
    print(f'avg_diff: {avg_diff}')
    print(f'num_gt10: {num_gt10}')

def odv_ort_to_str(odv_ort, mark1, mark2):
    return '\n'.join([f'{mark1}_{node1}\t{mark2}_{node2}\t{score}' for score, node1, node2 in odv_ort])


if __name__ == '__main__':
    from graph_helpers import get_graph_path, read_in_adj_set
    from analysis_helpers import get_deg_distr, print_deg_distr

    gtag1 = sys.argv[1]
    gtag2 = sys.argv[2]
    left = True
    nodes_gtag = gtag1 if left else gtag2

    path = '/home/wangph1/vmcopy/copy/mouse-rat-k4-n5000.ort'
    nodes = odv_ort_file_to_nodes(path, left)
    adj_set = read_in_adj_set(get_graph_path(nodes_gtag))
    deg_distr = get_deg_distr(nodes, adj_set)
    print_deg_distr(deg_distr)
