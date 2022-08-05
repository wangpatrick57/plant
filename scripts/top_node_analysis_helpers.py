#!/pkg/python/3.7.4/bin/python3
from graph_helpers import *
from ortholog_helpers import *

cached_adj_sets = dict()

def cache_read_in_adj_set(gtag):
    if gtag not in cached_adj_sets:
        cached_adj_sets[gtag] = read_in_adj_set(get_graph_path(gtag))

    return cached_adj_sets[gtag]

def get_top_nodes(adj_set, n):
    degrees = [(node, len(neighs)) for node, neighs in adj_set.items()]
    degrees.sort(key=(lambda data : data[1]), reverse=True)
    return degrees[:n]

def get_top_nodes_el(gtag, n, output_as_nodes):
    adj_set = cache_read_in_adj_set(gtag)
    top_nodes = get_top_nodes(adj_set, n)
    top_nodes_dict = {node: i for i, (node, degree) in enumerate(top_nodes)}
    el = []

    for node, degree in top_nodes:
        for neigh in adj_set[node]:
            if neigh in top_nodes_dict:
                if (output_as_nodes):
                    node1 = node
                    node2 = neigh
                    el.append((node1, node2))
                else:
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

if __name__ == '__main__':
    path = get_graph_path('slashdotaug_5v1')
    el = read_in_el(path)
    adj_set = adj_set_of_el(el)
    top_nodes = get_top_nodes(adj_set, 5)
    sg = induced_subgraph(el, [node for node, deg in top_nodes])
    print(top_nodes)
    print_el(sg)
