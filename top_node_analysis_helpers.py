#!/pkg/python/3.7.4/bin/python3
from graph_helpers import *
from ortholog_helpers import *
from odv_helpers import *

cached_adj_sets = dict()

def cache_read_in_adj_set(gtag):
    if gtag not in cached_adj_sets:
        cached_adj_sets[gtag] = read_in_adj_set(get_graph_path(gtag))

    return cached_adj_sets[gtag]

def get_top_nodes(adj_set, n):
    degrees = [(node, len(neighs)) for node, neighs in adj_set.items()]
    degrees.sort(key=(lambda data : data[1]), reverse=True)
    return degrees[:n]

def convert_top_nodes_to_ranked_nodes(top_nodes):
    return {node: rank for rank, (node, deg) in enumerate(top_nodes)}

def get_top_nodes_el(gtag, n):
    adj_set = cache_read_in_adj_set(gtag)
    top_nodes = get_top_nodes(adj_set, n)
    top_nodes_dict = {node: i for i, (node, degree) in enumerate(top_nodes)}
    el = []

    for node, degree in top_nodes:
        for neigh in adj_set[node]:
            if neigh in top_nodes_dict:
                node1 = f'{gtag[0:3]}{top_nodes_dict[node]}'
                node2 = f'{gtag[0:3]}{top_nodes_dict[neigh]}'
                el.append((node1, node2))

    el = clean_el(el)
    return el

def analyze_top_nodes_similarity(gtag1, gtag2, n):
    s1_adj_set = cache_read_in_adj_set(gtag1)
    s2_adj_set = cache_read_in_adj_set(gtag2)
    s1_top_nodes = get_top_nodes(s1_adj_set, n)
    s2_top_nodes = get_top_nodes(s2_adj_set, n)
    num_matches = 0
    num_total = 0

    for i in range(n):
        s1_node1 = s1_top_nodes[i][0]
        s2_node1 = s2_top_nodes[i][0]

        for j in range(i + 1, n):
            s1_node2 = s1_top_nodes[j][0]
            s2_node2 = s2_top_nodes[j][0]
            s1_has_edge = s1_node1 in s1_adj_set[s1_node2] or s1_node2 in s1_adj_set[s1_node1]
            s2_has_edge = s2_node1 in s2_adj_set[s2_node2] or s2_node2 in s2_adj_set[s2_node1]
            num_matches += 1 if s1_has_edge == s2_has_edge else 0
            num_total += 1

    return (num_matches, num_total)

def get_top_nodes_of_gtag(gtag, n):
    path = get_graph_path(gtag)
    el = read_in_el(path)
    adj_set = adj_set_of_el(el)
    top_nodes = get_top_nodes(adj_set, n)
    return top_nodes

def get_ranked_nodes_of_gtag(gtag, n):
    top_nodes = get_top_nodes_of_gtag(gtag, n)
    ranked_nodes = convert_top_nodes_to_ranked_nodes(top_nodes)
    return ranked_nodes

def compare_top_nodes_in_alignment(gtag1, gtag2, alignment, top_cutoff):
    all_ranked_nodes1 = get_ranked_nodes_of_gtag(gtag1, gtag_to_n(gtag1))
    all_ranked_nodes2 = get_ranked_nodes_of_gtag(gtag2, gtag_to_n(gtag2))
    sep = '\t'

    print(gtag1, gtag2, sep=sep)
    
    for node1, node2 in alignment:
        assert node1 in all_ranked_nodes1, f'{node1} not in all_ranked_nodes1'
        assert node2 in all_ranked_nodes2, f'{node2} not in all_ranked_nodes2'
        node1_rank = all_ranked_nodes1[node1]
        node2_rank = all_ranked_nodes2[node2]

        if node1_rank < top_cutoff or node2_rank < top_cutoff:
            print(f'{node1}(rank:{node1_rank})', f'{node2}(rank:{node2_rank})', sep=sep)

if __name__ == '__main__':
    gtag1 = 'mouse'
    gtag2 = 'rat'
    compare_top_nodes_in_alignment(gtag1, gtag2, get_g1_to_g2_orthologs_as_alignment(gtag1, gtag2), 10)
