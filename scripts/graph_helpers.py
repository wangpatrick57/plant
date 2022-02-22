import re

def all_species():
    return ['cat', 'chicken', 'cow', 'dog', 'duck', 'guinea_pig', 'horse', 'human', 'mouse', 'pig', 'rabbit', 'rat', 'sheep', 'turkey']

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

def read_in_el(graph_fname):
    el = []
    graph_file = open(graph_fname, 'r')

    for line in graph_file:
        node1, node2 = line.strip().split('\t')
        el.append((node1, node2))

    graph_file.close()
    return el

def read_nodes(graph_file):
    nodes = set()

    for edge_str in graph_file:
        node1, node2 = re.split('[\s\t]', edge_str.strip())
        nodes.add(node1)
        nodes.add(node2)

    return nodes
