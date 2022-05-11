#!/pkg/python/3.7.4/bin/python3
from graph_helpers import *
from ortholog_helpers import *

def get_top_num(adj_set, n):
    degrees = [(node, len(neighs)) for node, neighs in adj_set.items()]
    degrees.sort(key=(lambda data : data[1]), reverse=True)
    return degrees[:n]

def top_num_analyze(species1, species2, n):
    s1_graph_path = get_graph_path(species1)
    s2_graph_path = get_graph_path(species2)
    s1_adj_set = read_in_adj_set(s1_graph_path)
    s2_adj_set = read_in_adj_set(s2_graph_path)
    s1_top_num = get_top_num(s1_adj_set, n)
    s2_top_num = get_top_num(s2_adj_set, n)
    num_matches = 0
    num_total = 0

    for i in range(n):
        s1_node1 = s1_top_num[i][0]
        s2_node1 = s2_top_num[i][0]

        for j in range(i + 1, n):
            s1_node2 = s1_top_num[j][0]
            s2_node2 = s2_top_num[j][0]
            s1_has_edge = s1_node1 in s1_adj_set[s1_node2] or s1_node2 in s1_adj_set[s1_node1]
            s2_has_edge = s2_node1 in s2_adj_set[s2_node2] or s2_node2 in s2_adj_set[s2_node1]
            num_matches += 1 if s1_has_edge == s2_has_edge else 0
            num_total += 1

    print(f'{species1}&{species2}: {num_matches} / {num_total}')

if __name__ == '__main__':
    species = ['cat', 'cow', 'mouse', 'rat', 'human']

    for i in range(len(species)):
        species1 = species[i]

        for j in range(i + 1, len(species)):
            species2 = species[j]

            top_num_analyze(species1, species2, 5)
