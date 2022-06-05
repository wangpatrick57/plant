#!/pkg/python/3.7.4/bin/python3
import sys
import random
import datetime
import profile
from collections import defaultdict
from graph_helpers import *

# sample rates
#  * 0.00002 for IIDmouse k=8 lDEG=2
SAMPLE_RATE = 1

def parse_rank_str(rank_str):
    if rank_str == None:
        return None

    return [int(r) for r in rank_str.split(' -> ')]
RANK_PATH_FILTER = parse_rank_str(None)
NODE_PATH_FILTER = None
WHITELISTED_NODES_FILTER = ['NUP1', 'RPS22A', 'RRP40', 'RRP6', 'SRP1', 'STO1']

sample_rate_cache = dict()

def get_sample_rate(k):
    if k not in sample_rate_cache:
        sample_rate_cache[k] = SAMPLE_RATE ** (1 / k)
        print(f'sample rate for {k}: {sample_rate_cache[k]}')

    return sample_rate_cache[k]

def path_str(l):
    return ' -> '.join([str(e) for e in l])

def get_ranks(sorted_nodes, heurs):
    ranks = dict()
    curr_rank = -1
    last_heur = None

    for i, node in enumerate(sorted_nodes, 1):
        heur = heurs[node]

        if heur != last_heur:
            curr_rank = i

        ranks[node] = curr_rank
        last_heur = heur

    return ranks

class RankPathTracker:
    def __init__(self, nodes, heurs, alph):
        sorted_nodes = blant_sorted(nodes, heurs, alph)
        self._ranks = get_ranks(sorted_nodes, heurs)
        self._rank_paths = []
        
    def print_ranks(self):
        reverse_dict = defaultdict(list)

        for node, rank in self._ranks.items():
            reverse_dict[rank].append(node)

        sorted_ranks = sorted(self._ranks.values(), reverse=True)

        for rank in sorted_ranks:
            print(f'{rank}: {reverse_dict[rank]}')

    def get_rank(self, node):
        return self._ranks[node]

    def track(self, nodes):
        rank_path = []

        for node in nodes:
            rank_path.append(self._ranks[node])

        self._rank_paths.append(rank_path)
 
    def report(self):
        for path in self._rank_paths:
            print(path_str(path))

def blant_sorted(nodes, heurs, alph):
    nwhs = [(node, heurs[node]) for node in nodes]

    if alph:
        nwhs.sort(key=(lambda nwh: (-nwh[1], nwh[0])))
    else:
        nwhs.sort(key=(lambda nwh: (nwh[1], nwh[0])), reverse=True)

    return [node for node, heur in nwhs]

def get_deg_heurs(nodes, adj_set):
    heurs = dict()

    for node in nodes:
        heurs[node] = len(adj_set[node])

    return heurs

def canon(nodes):
    return sorted(nodes)

def rank_path_filter_blocks(prev_nodes, prev_nodes_count, rpt):
    pos = prev_nodes_count - 1
    latest_node = prev_nodes[pos]
    ignore = pos >= len(RANK_PATH_FILTER) or RANK_PATH_FILTER[pos] == None
    return not ignore and RANK_PATH_FILTER[pos] != rpt.get_rank(latest_node)

def node_path_filter_blocks(prev_nodes, prev_nodes_count):
    pos = prev_nodes_count - 1
    latest_node = prev_nodes[pos]
    ignore = pos >= len(NODE_PATH_FILTER) or NODE_PATH_FILTER[pos] == None
    return not ignore and NODE_PATH_FILTER[pos] != latest_node

def whitelisted_nodes_filter_blocks(prev_nodes, prev_nodes_count):
    return not any([in_prev_nodes(prev_nodes, prev_nodes_count, whitelisted_node) for whitelisted_node in WHITELISTED_NODES_FILTER])

def sample_filter_blocks(k):
    return random.random() >= get_sample_rate(k)

def in_prev_nodes(prev_nodes, prev_nodes_count, node):
    for i in range(prev_nodes_count):
        if prev_nodes[i] == node:
            return True

    return False

def blant_expand(prev_nodes, prev_nodes_count, k, lDEG, alph, adj_set, heurs, results, rpt=None, print_tree=False, print_path_of=None):
    # check filters
    if NODE_PATH_FILTER != None:
        if node_path_filter_blocks(prev_nodes, prev_nodes_count):
            return

    if WHITELISTED_NODES_FILTER != None:
        if whitelisted_nodes_filter_blocks(prev_nodes, prev_nodes_count):
            return

    if RANK_PATH_FILTER != None:
        # if rank filter is not none, we will just assume that an rpt is available to take the rank from
        if rank_path_filter_blocks(prev_nodes, prev_nodes_count, rpt):
            return

    if SAMPLE_RATE != None:
        if sample_filter_blocks(k):
            return

    # base case
    if prev_nodes_count == k:
        results.add(tuple(canon(prev_nodes)))

        if rpt != None:
            rpt.track(prev_nodes)

        if print_path_of != None:
            if sorted(prev_nodes) == sorted(print_path_of):
                print(path_str(prev_nodes))
 
        return

    expand_set = set()

    for i in range(prev_nodes_count):
        node = prev_nodes[i]

        for neigh in adj_set[node]:
            if not in_prev_nodes(prev_nodes, prev_nodes_count, neigh):
                expand_set.add(neigh)

    expand_list = blant_sorted(list(expand_set), heurs, alph)
    expanded_heurs = set()
    pretabs = '\t' * prev_nodes_count

    for to_expand in expand_list:
        expanded_heurs.add(heurs[to_expand])

        if len(expanded_heurs) > lDEG:
            break

        if print_tree:
            print(f'{pretabs}{to_expand}')

        prev_nodes[prev_nodes_count] = to_expand
        blant_expand(prev_nodes, prev_nodes_count + 1, k, lDEG, alph, adj_set, heurs, results, rpt=rpt, print_tree=print_tree, print_path_of=print_path_of)

def run_blant(el, k=8, lDEG=2, alph=True, use_rpt=False, print_tree=False, print_progress=None, print_path_of=None):
    nodes = nodes_of_el(el)
    adj_set = adj_set_of_el(el)
    heurs = get_deg_heurs(nodes, adj_set)

    # trackers
    rpt = RankPathTracker(nodes, heurs, alph) if use_rpt else None

    sorted_nodes = blant_sorted(nodes, heurs, alph)
    num_nodes = len(sorted_nodes)
    print('all setup done')
    graphlets = set()
    prev_nodes = [None] * k

    if print_progress != None:
        node_count = 0
        last_printed = -1

    for node in sorted_nodes:
        results = set()
        prev_nodes[0] = node

        if print_tree:
            print(node)

        if print_progress != None:
            node_count += 1
            curr_print_val = int(node_count * print_progress / len(sorted_nodes))

            if curr_print_val > last_printed:
                last_printed = curr_print_val
                print(f'done: {curr_print_val} / {print_progress}')

        blant_expand(prev_nodes, 1, k, lDEG, alph, adj_set, heurs, results, rpt=rpt, print_tree=print_tree, print_path_of=print_path_of)
        graphlets = graphlets.union(results)

    if use_rpt:
        rpt.report()

    return graphlets

def graphlets_str(graphlets):
    return '\n'.join([' '.join(graphlet) for graphlet in graphlets])

if __name__ == '__main__':
    seed = int(datetime.datetime.now().timestamp())
    print(f'using seed {seed}')
    random.seed(seed)
    path = get_gtag_graph_path('syeast0')
    el = read_in_el(path)
    print('el read in')
    sys.setrecursionlimit(100000)
    k = 6
    graphlets = run_blant(el, k=k, lDEG=2, use_rpt=True, print_tree=False, print_progress=None, print_path_of=None)
    print(len(graphlets))
    write_to_file(graphlets_str(graphlets), f'test_py_sy0_k{k}l2.out')
