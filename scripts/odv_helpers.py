#!/pkg/python/3.7.4/bin/python3
import sys
import math
import heapq
from collections import defaultdict
from statistics import mean
from bash_helpers import *
from graph_helpers import *

NUM_GRAPHLETS = 30
NUM_ORBITS = 73

def get_odv_path(species, k):
    return get_data_path(f'odv/{species}-k{k}.odv')

def calc_orbit_counts():
    USE_CACHE = False

    if USE_CACHE:
        return [1, 2, 2, 2, 3, 4, 3, 3, 4, 3, 4, 4, 4, 4, 3, 4, 6, 5, 4, 5, 6, 6, 4, 4, 5, 5, 8, 4, 6, 6, 7, 5, 6, 6, 6, 5, 6, 7, 7, 5, 7, 7, 7, 6, 5, 5, 6, 8, 8, 6, 6, 8, 6, 9, 6, 6, 4, 6, 6, 8, 9, 6, 6, 8, 8, 6, 7, 7, 8, 5, 6, 6, 4]
    else:
        orbit_counts = [None] * NUM_ORBITS

        for graphlet_num in range(NUM_GRAPHLETS):
            p = run_orca(5, get_base_graph_path(f'graphlets/graphlet{graphlet_num}'))
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

def calc_weights():
    orbit_counts = calc_orbit_counts()
    weights = [1 - math.log(orbit_count) / math.log(NUM_ORBITS) for orbit_count in orbit_counts]
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
            odv = ODV(odv_list)
            self._directory[node] = odv

    def get_odv(self, node):
        return self._directory[node]

    def get_nodes(self):
        return self._directory.keys()

    def __str__(self):
        return '\n'.join([f'{node}: {odv}' for node, odv in self._directory.items()])


class ODV:
    WEIGHTS = calc_weights()
    WEIGHT_SUM = sum(WEIGHTS) # 45.08670802954777# sum(WEIGHTS)

    def __init__(self, odv_list):
        self._odv_list = odv_list

    def get_similarity(self, other):
        assert len(self._odv_list) == len(other._odv_list) == len(ODV.WEIGHTS), f'self: {len(self._odv_list)}, other: {len(other._odv_list)}, weights: {len(ODV.WEIGHTS)}'
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

def get_odv_orthologs(gtag1, gtag2, n, k):
    graph_path1 = get_gtag_graph_path(gtag1)
    graph_path2 = get_gtag_graph_path(gtag2)
    nodes1 = read_in_nodes(graph_path1)
    nodes2 = read_in_nodes(graph_path2)
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

    for node1 in nodes1:
        for node2 in nodes2:
            odv1 = odv_dir1.get_odv(node1)
            odv2 = odv_dir2.get_odv(node2)
            sim = odv1.get_similarity(odv2)
            min_node = min(node1, node2)
            max_node = max(node1, node2)
            obj = (sim, min_node, max_node)
            min_top = heapq.heappushpop(top_n, obj)
        
        proc_nodes += 1

        if proc_nodes * 100 / tot_nodes > percent_printed:
            percent_printed += 1
            print(f'{percent_printed}% done', file=sys.stderr)

        if percent_printed >= 5:
            break

    return sorted(top_n, reverse=True)

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

def gen_fake_ort_from_sim(base, k, n):
    sim_path = get_fake_ort_path(base, 'sim')
    ort_path = get_fake_ort_path(f'{base}-{k}', 'ort')
    added_nodes = set()

    with open(sim_path, 'r') as sim_f:
        with open(ort_path, 'w') as ort_f:
            i = 0

            for line in sim_f:
                node1, node2, score = line.split()
                marked_node2 = f'sy20_{node2}'

                if i < k:
                    added_nodes.add(node1)
                    added_nodes.add(node2)
                    ort_f.write('\t'.join([node1, marked_node2, score]) + '\n')
                    i += 1
                else:
                    if node1 not in added_nodes or node2 not in added_nodes:
                        added_nodes.add(node1)
                        added_nodes.add(node2)
                        ort_f.write('\t'.join([node1, marked_node2, score]) + '\n')

                    if len(added_nodes) >= n:
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
            
            if tot_pairs > 1_300:
                break

            inequal_orbits = odv1.get_inequal_orbits(odv2)

            if len(inequal_orbits) < 4:
                print(f'tot{tot_pairs}p')
                print(f'{node1}-{node2}: {abs(sim_non_decimal - my_sim_non_decimal)}')
                print(f'\tdiffs: {inequal_orbits}')

    avg_diff = (tot_diff / tot_pairs) / FACTOR
    print(f'avg_diff: {avg_diff}')
    print(f'num_gt10: {num_gt10}')

def odv_ort_to_str(odv_ort):
    return '\n'.join([f'{node1}\t{node2}\t{score}' for score, node1, node2 in odv_ort])


if __name__ == '__main__':
    # calc_orbit_counts()
    gtag1 = sys.argv[1]
    gtag2 = sys.argv[2]
    k = sys.argv[3]
    n = 5000
    odv_ort = get_odv_orthologs(gtag1, gtag2, n, k)
    write_to_file(odv_ort_to_str(odv_ort), get_fake_ort_path(f'{gtag1}-{gtag2}-k{k}-n{n}', 'myort'))
