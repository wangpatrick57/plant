#!/pkg/python/3.7.4/bin/python3
import copy
import sys
from graph_helpers import *

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

def blant_expand(prev_nodes, k, lDEG, alph, adj_set, heurs, results):
    if len(prev_nodes) == k:
        results.append(copy.copy(prev_nodes))
        return

    all_neighs = set()

    for node in prev_nodes:
        for neigh in adj_set[node]:
            all_neighs.add(neigh)

    all_neighs = blant_sorted(list(all_neighs), heurs, alph)
    expanded_heurs = set()

    for neigh in all_neighs:
        expanded_heurs.add(heurs[neigh])

        if len(expanded_heurs) > lDEG:
            break

        prev_nodes.append(neigh)
        blant_expand(prev_nodes, k, lDEG, alph, adj_set, heurs, results)
        prev_nodes = prev_nodes[:-1]

def run_blant(el, k=8, lDEG=2, alph=True):
    nodes = nodes_of_el(el)
    adj_set = adj_set_of_el(el)
    heurs = get_deg_heurs(nodes, adj_set)
    sorted_nodes = blant_sorted(nodes, heurs, alph)

    for node in sorted_nodes:
        results = []
        blant_expand([node], k, lDEG, alph, adj_set, heurs, results)
        print('\n'.join([' '.join(graphlet) for graphlet in results]))

if __name__ == '__main__':
    path = get_gtag_graph_path('syeast0')
    el = read_in_el(path)
    sys.setrecursionlimit(10000)
    run_blant(el, k=8)
