#!/pkg/python/3.7.4/bin/python3
from graph_helpers import *
from ortholog_helpers import *

cached_adj_sets = dict()

def cache_read_in_adj_set(species):
    if species not in cached_adj_sets:
        cached_adj_sets[species] = read_in_adj_set(get_graph_path(species))

    return cached_adj_sets[species]

def get_top_nodes(adj_set, n):
    degrees = [(node, len(neighs)) for node, neighs in adj_set.items()]
    degrees.sort(key=(lambda data : data[1]), reverse=True)
    return degrees[:n]

def get_top_nodes_el(species, n):
    adj_set = cache_read_in_adj_set(species)
    top_nodes = get_top_nodes(adj_set, n)
    top_nodes_dict = {node: i for i, (node, degree) in enumerate(top_nodes)}
    el = []

    for node, degree in top_nodes:
        for neigh in adj_set[node]:
            if neigh in top_nodes_dict:
                node1 = f'{species[0:3]}{top_nodes_dict[node]}'
                node2 = f'{species[0:3]}{top_nodes_dict[neigh]}'
                el.append((node1, node2))

    el = clean_el(el)
    return el

def analyze_top_nodes_similarity(species1, species2, n):
    s1_adj_set = cache_read_in_adj_set(species1)
    s2_adj_set = cache_read_in_adj_set(species2)
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
    # species_pairs = [('cow', 'human'), ('guinea_pig', 'human'), ('rat', 'human'), ('dog', 'human'), ('guinea_pig', 'horse'), ('horse', 'rat'), ('horse', 'dog'), ('cat', 'horse'), ('cow', 'mouse'), ('guinea_pig', 'mouse'), ('cat', 'mouse'), ('guinea_pig', 'rat'), ('guinea_pig', 'dog'), ('guinea_pig', 'cat'), ('guinea_pig', 'cow'), ('cow', 'rat'), ('dog', 'cow'), ('cat', 'cow'), ('dog', 'rat'), ('cat', 'rat'), ('cat', 'dog')]

    el = get_top_nodes_el('guinea_pig', 6)
    print_el(el)
