import re

def all_species():
    return ['cat', 'chicken', 'cow', 'dog', 'duck', 'guinea_pig', 'horse', 'human', 'mouse', 'pig', 'rabbit', 'rat', 'sheep', 'turkey']

def get_graph_path(species):
    if 'syeast' in species:
        return f'/home/wangph1/BLANT/networks/{species}/{species}.el'
    else:
        return f'/home/sana/Jurisica/IID/networks/IID{species}.el'

def get_notopedge_graph_path(species):
    return f'/home/wangph1/plant/networks/paper/IID{species}_without_top_edge.el'

def get_snap_graph_path(name):
    return f'/home/wangph1/plant/networks/snap/{name}'

def read_in_adj_set(graph_path):
    with open(graph_path, 'r') as graph_file:
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

def read_in_el(graph_path):
    el = []
    graph_file = open(graph_path, 'r')

    for line in graph_file:
        node1, node2 = re.split('[\s\t]', line.strip())
        el.append((node1, node2))

    graph_file.close()
    return el

# if you need to read in nodes of a temporal graph, refactor this to call a helper function called read_in_nodes_logic which takes in an el
def read_in_nodes(graph_path):
    nodes = set()
    graph_file = open(graph_path, 'r')

    for edge_str in graph_file:
        node1, node2 = re.split('[\s\t]', edge_str.strip())
        nodes.add(node1)
        nodes.add(node2)

    graph_file.close()
    return nodes
