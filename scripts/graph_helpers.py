import re

def get_graph_fname_from_species(species):
    return f'/home/sana/Jurisica/IID/networks/IID{species}.el'

def read_adj_set(graph_file):
    adj_set = dict()

    for edge_str in graph_file:
        node1, node2 = re.split('[\s\t]', edge_str.strip())

        if node1 not in adj_set:
            adj_set[node1] = set()

        if node2 not in adj_set:
            adj_set[node2] = set()

        adj_set[node1].add(node2)
        adj_set[node2].add(node1)

    return adj_set
