#!/pkg/python/3.7.4/bin/python3
import re
import random
import networkx as nx
import sys
from file_helpers import *

def get_all_iid_mammals():
    return ['cat', 'cow', 'dog', 'guinea_pig', 'horse', 'human', 'mouse', 'pig', 'rabbit', 'rat', 'sheep']

def is_species(gtag):
    return gtag in get_all_iid_mammals() or 'syeast' in gtag

def get_gtag_graph_path(gtag):
    if is_species(gtag):
        return get_graph_path(gtag)
    else:
        return get_snap_graph_path(gtag)

def get_graph_path(species):
    if 'syeast' in species:
        return f'/home/wangph1/BLANT/networks/{species}/{species}.el'
    else:
        return f'/home/sana/Jurisica/IID/networks/IID{species}.el'

def get_notopedge_graph_path(species):
    return f'/home/wangph1/plant/networks/paper/IID{species}_without_top_edge.el'

def get_snap_graph_path(snap):
    return f'/home/wangph1/plant/networks/snap/{snap}.el'

def read_in_adj_set(graph_path):
    return adj_set_of_el(read_in_el(graph_path))

def read_in_el(graph_path):
    el = []
    graph_file = open(graph_path, 'r')

    for line in graph_file:
        node1, node2 = re.split('[\s\t]', line.strip())
        el.append((node1, node2))

    graph_file.close()
    return clean_el(el)

# if you need to read in nodes of a temporal graph, refactor this to call a helper function called read_in_nodes_logic which takes in an el
def read_in_nodes(graph_path):
    return nodes_of_el(read_in_el(graph_path))

def nodes_of_el(el):
    nodes = set()

    for node1, node2 in el:
        nodes.add(node1)
        nodes.add(node2)

    return nodes

def adj_set_of_el(el):
    adj_set = dict()

    for node1, node2 in el:
        if node1 not in adj_set:
            adj_set[node1] = set()

        if node2 not in adj_set:
            adj_set[node2] = set()

        adj_set[node1].add(node2)
        adj_set[node2].add(node1)

    return adj_set

def read_in_seeds(seeds_path):
    seeds = set()
    seeds_file = open(seeds_path, 'r')

    for line in seeds_file:
        node1, node2 = re.split('[\s\t]', line.strip())
        seeds.add((node1, node2))

    return list(seeds)

def graph_stats(el, name='graph', verbose=False):
    nodes = set()
    edges = set()

    for node1, node2 in el:
        nodes.add(node1)
        nodes.add(node2)
        edges.add((node1, node2))

    if verbose:
        print()
        print(f'=== {name} ===')
        print(f'NUM NODES: {len(nodes)}')
        print(f'NUM EDGES: {len(edges)}')
    else:
        print(f'{name}: {len(nodes)}n - {len(edges)}e')

def clean_el(el):
    edges = set()

    for node1, node2 in el:
        if node1 != node2:
            min_node = min(node1, node2)
            max_node = max(node1, node2)
            edges.add((min_node, max_node))

    el = list(edges)
    return el

def el_remove_node(el, node):
    new_el = []

    for node1, node2 in el:
        if node1 != node and node2 != node:
            new_el.append((node1, node2))
    
    return new_el

def print_adj_set_sorted(adj_set):
    lengths = [(node, len(neighs)) for node, neighs in adj_set.items()]
    lengths.sort(key=(lambda e : e[1]))
    print('\n'.join(f'{node} has degree {length}' for node, length in lengths))

def print_el(el):
    print('\n'.join(f'{node1}\t{node2}' for node1, node2 in el))

def print_xel(xel):
    print('\n'.join('\t'.join([e for e in edge]) for edge in xel))

def el_to_nxg(el):
    nxg = nx.Graph()

    for node1, node2 in el:
        nxg.add_edge(node1, node2)

    return nxg

def get_ccs_list(nxg):
    return nx.connected_components(nxg)

def soften_el(el, r):
    soft_el = []

    for edge in el:
        if random.random() >= r:
            soft_el.append(edge)

    return soft_el

def induced_subgraph(el, nodes):
    sg = []
    nodes_set = set(nodes)

    for node1, node2 in el:
        if node1 in nodes_set and node2 in nodes_set:
            sg.append((node1, node2))

    return clean_el(sg)

if __name__ == '__main__':
    base = sys.argv[1]
    el = read_in_el(get_snap_graph_path(base))
    soft5v1_el = soften_el(el, 0.05)
    soft5v2_el = soften_el(el, 0.05)
    soft10v1_el = soften_el(el, 0.1)
    soft10v2_el = soften_el(el, 0.1)
    els = [soft5v1_el, soft5v2_el, soft10v1_el, soft10v2_el]
    adds = ['_5v1', '_5v2', '_10v1', '_10v2']

    for this_el, this_add in zip(els, adds):
        graph_stats(this_el, f'{base}{this_add}')
        write_el_to_file(this_el, get_snap_graph_path(f'{base}{this_add}'))
