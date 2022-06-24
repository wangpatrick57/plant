#!/pkg/python/3.7.4/bin/python3
import re
import random
import networkx as nx
import sys
from collections import defaultdict
from file_helpers import *
from el_conv import *

NETWORKS_DIR = '/home/wangph1/plant/networks'

def get_all_iid_mammals():
    return ['cat', 'cow', 'dog', 'guineapig', 'horse', 'human', 'mouse', 'pig', 'rabbit', 'rat', 'sheep']

def get_all_iid_nonmammals():
    return ['fly', 'worm']

def get_all_iid_species():
    return get_all_iid_mammals() + get_all_iid_nonmammals()

def get_all_syeasts():
    return ['syeast0', 'syeast05', 'syeast10', 'syeast15', 'syeast20', 'syeast25']

def get_paper_nontprl_snap():
    social = ['facebook', 'git']
    collab = ['astroph', 'cond']
    citat = ['hepph', 'hepth']
    comm = ['enron']
    auto = ['caida', 'oreg2']
    p2p = ['gnu24', 'gnu30']
    return social + collab + citat + comm + auto + p2p

def get_paper_tprl_snap():
    return ['reddit', 'sxso', 'math', 'super', 'ubuntu', 'wiki', 'email', 'college', 'otc', 'alpha']

def get_syeast_pairs():
    pairs = []
    syeasts = get_all_syeasts()
    syeast0 = syeasts[0]
    syeast_others = syeasts[1:]

    for other in syeast_others:
        pairs.append((syeast0, other))

    return pairs

def get_iid_mammal_pairs():
    pairs = []
    mammals = get_all_iid_mammals()

    for i in range(len(mammals)):
        for j in range(i + 1, len(mammals)):
            pairs.append((mammals[i], mammals[j]))

    return pairs

def get_tprl_pairs():
    from temporal_graph_helpers import get_std_percents, get_gtag_from_tgtag

    pairs = []
    tprls = get_paper_tprl_snap()
    percents = get_std_percents()
    percent0 = percents[0]
    percent_others = percents[1:]

    for tgtag in tprls:
        for other in percent_others:
            p0_gtag = get_gtag_from_tgtag(tgtag, percent0)
            other_gtag = get_gtag_from_tgtag(tgtag, other)
            pairs.append((p0_gtag, other_gtag))

    return pairs

def get_paper_all_pairs():
    syeast_pairs = get_syeast_pairs()
    iid_pairs = get_iid_mammal_pairs()
    tprl_pairs = get_tprl_pairs()
    return syeast_pairs + iid_pairs + tprl_pairs

def is_paper_snap(gtag):
    return gtag in get_paper_nontprl_snap() or gtag in get_paper_tprl_snap()

def get_marked_node(gtag, node):
    return f'{gtag_to_mark(gtag)}_{node}'

def unmark_node(node):
    return '_'.join(node.split('_')[1:])

def get_marked_el(gtag):
    path = get_graph_path(gtag)
    el = read_in_el(path)
    marked_el = []

    for node1, node2 in el:
        marked_el.append((get_marked_node(gtag, node1), get_marked_node(gtag, node2)))

    return marked_el

def check_all_marks_unique(gtags):
    num_gtags = len(set(gtags))
    marks = [gtag_to_mark(gtag) for gtag in gtags]
    mark_dupes = defaultdict(int)

    for mark in marks:
        mark_dupes[mark] += 1
    
    num_marks = len(mark_dupes)

    if num_gtags == num_marks:
        print('all marks unique')
    else:
        print('some marks are duplicate')
        print('\n'.join([f'{mark}: {cnt}' for mark, cnt in mark_dupes.items() if cnt > 1]))

def get_paper_base_gtags():
    iid_species = get_all_iid_species()
    syeasts = get_all_syeasts()
    nontprl_snap = get_paper_nontprl_snap()
    tprl_snap = get_paper_tprl_snap()
    return iid_mammals + syeasts + nontprl_snap + tprl_snap

def is_species(gtag):
    base_gtag = gtag.split('_')[0]
    return base_gtag in get_all_iid_species() or 'syeast' in base_gtag

def is_iid_species(gtag):
    return gtag in get_all_iid_species()

def get_graph_path(gtag):
    from noise_helpers import is_noisy_gtag, get_noisy_graph_path

    if gtag == 'tester':
        return get_base_graph_path(gtag)
    elif gtag in {'alphabet', 'alpha10'}:
        return get_custom_graph_path(gtag)
    elif '_adv' in gtag:
        return get_adv_graph_path(gtag)
    elif is_noisy_gtag(gtag):
        return get_noisy_graph_path(gtag)
    elif is_species(gtag):
        return get_species_graph_path(gtag)
    else:
        return get_snap_graph_path(gtag)

def get_nif_path(gtag):
    return get_base_graph_path(f'mcl/{gtag}_marked', ext='nif')

def split_gtag(gtag):
    splitted = gtag.split('_')
    base_gtag = splitted[0]
    mods = splitted[1:]
    return base_gtag, mods

def gtag_to_mark(gtag):
    base_gtag, mods = split_gtag(gtag)
    mark = base_gtag_to_mark(base_gtag)
    
    for mod in mods:
        mark += mod

    return mark

def base_gtag_to_mark(gtag):
    if gtag == 'syeast0':
        return 'sy0'
    elif gtag == 'syeast05':
        return 'sy5'
    elif gtag == 'syeast10':
        return 'sy10'
    elif gtag == 'syeast15':
        return 'sy15'
    elif gtag == 'syeast20':
        return 'sy20'
    elif gtag == 'syeast25':
        return 'sy25'
    elif is_iid_species(gtag):
        return gtag[:3]
    elif is_paper_snap(gtag):
        if gtag == 'hepph':
            return 'hph'
        elif gtag == 'hepth':
            return 'hth'
        elif gtag == 'gnu24':
            return 'g24'
        elif gtag == 'gnu30':
            return 'g30'
        else:
            return gtag[:3]

def get_base_graph_path(name, ext='el'):
    return f'{NETWORKS_DIR}/{name}.{ext}'

def get_custom_graph_path(name):
    return get_base_graph_path(f'custom/{name}')

def get_adv_gtag(gtag, i):
    return f'{gtag}_adv{i}'

def get_adv_graph_path(adv_gtag):
    return get_base_graph_path(f'adversarial/{adv_gtag}')

def is_syeast(species):
    return 'syeast' in species

def get_species_graph_path(species):
    if is_syeast(species):
        return get_base_graph_path(f'syeast/{species}')
    else:
        return get_base_graph_path(f'iid/{species}')

def get_snap_graph_path(snap):
    return f'{NETWORKS_DIR}/snap/{snap}.el'

def read_in_adj_set(graph_path):
    return adj_set_of_el(read_in_el(graph_path))

def get_max_deg(adj_set):
    return max([len(neighs) for neighs in adj_set.values()])

def read_in_el(graph_path):
    el = []
    graph_file = open(graph_path, 'r')

    for line in graph_file:
        node1, node2 = re.split('[\s\t]', line.strip())
        el.append((node1, node2))

    graph_file.close()
    return clean_el(el)

def el_to_str(el):
    return '\n'.join([f'{node1}\t{node2}' for node1, node2 in el])

def in_edge_set(node1, node2, edge_set):
    return (node1, node2) in edge_set or (node2, node1) in edge_set

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
    gtag = sys.argv[1]
    el = get_marked_el(gtag)
    el = clean_el(el)
    path = get_graph_path(gtag)
    out_path = get_nif_path(gtag)
    print(out_path)
    write_to_file(get_nif_str(el), out_path)
