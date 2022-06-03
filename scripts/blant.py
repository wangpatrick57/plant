#!/pkg/python/3.7.4/bin/python3
import sys
import random
import datetime
from collections import defaultdict
from graph_helpers import *

# sample rates
#  * 0.00002 for IIDmouse k=8 lDEG=2
SAMPLE_RATE = 0.00002

def parse_rank_str(rank_str):
    if rank_str == None:
        return None

    return [int(r) for r in rank_str.split(' -> ')]
RANK_FILTER = parse_rank_str(None)

sample_rate_cache = dict()

def get_sample_rate(k):
    if k not in sample_rate_cache:
        sample_rate_cache[k] = SAMPLE_RATE ** (1 / k)
        print(f'sample rate for {k}: {sample_rate_cache[k]}')

    return sample_rate_cache[k]

class RankPathTracker:
    def __init__(self, nodes, heurs, alph):
        self._ranks = dict()
        self._rank_paths = []
        sorted_nodes = blant_sorted(nodes, heurs, alph)
        curr_rank = -1
        last_heur = None

        for i, node in enumerate(sorted_nodes, 1):
            heur = heurs[node]

            if heur != last_heur:
                curr_rank = i

            self._ranks[node] = curr_rank
            last_heur = heur

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
            print(' -> '.join([str(rank) for rank in path]))

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

def blant_expand(prev_nodes, k, lDEG, alph, adj_set, heurs, results, rpt=None):
    # check filters
    if RANK_FILTER != None:
        # if rank filter is one, we will just assume that an rpt is available to take the rank from
        pos = len(prev_nodes) - 1
        latest_node = prev_nodes[pos]
        ignore = pos >= len(RANK_FILTER) or RANK_FILTER[pos] == None

        if not ignore and RANK_FILTER[pos] != rpt.get_rank(latest_node):
            return
    elif SAMPLE_RATE != None:
        if random.random() >= get_sample_rate(k):
            return

    # base case
    if len(prev_nodes) == k:
        results.add(tuple(canon(prev_nodes)))

        if rpt != None:
            rpt.track(prev_nodes)
 
        return

    prev_nodes_set = set(prev_nodes)
    expand_set = set()

    for node in prev_nodes:
        for neigh in adj_set[node]:
            if neigh not in prev_nodes_set:
                expand_set.add(neigh)

    expand_list = blant_sorted(list(expand_set), heurs, alph)
    expanded_heurs = set()

    append = '\t' * len(prev_nodes)

    for to_expand in expand_list:
        expanded_heurs.add(heurs[to_expand])

        if len(expanded_heurs) > lDEG:
            break

        prev_nodes.append(to_expand)
        saved_len = len(prev_nodes)
        blant_expand(prev_nodes, k, lDEG, alph, adj_set, heurs, results, rpt=rpt)
        prev_nodes = prev_nodes[:saved_len] # TODO: see if we can remove this line and do prev_nodes[i] instead of append

def run_blant(el, k=8, lDEG=2, alph=True, use_rpt=False):
    nodes = nodes_of_el(el)
    adj_set = adj_set_of_el(el)
    heurs = get_deg_heurs(nodes, adj_set)

    if use_rpt:
        rpt = RankPathTracker(nodes, heurs, alph)
    else:
        rpt = None

    sorted_nodes = blant_sorted(nodes, heurs, alph)
    print('all setup done')
    graphlets = set()

    for node in sorted_nodes:
        results = set()
        blant_expand([node], k, lDEG, alph, adj_set, heurs, results, rpt=rpt)
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
    graphlets = run_blant(el, k=8, lDEG=2, use_rpt=True)
    # print(graphlets_str(graphlets))
