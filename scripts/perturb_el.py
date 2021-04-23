import sys
import re
import random
from collections import defaultdict

el_file = open(sys.argv[1], 'r')
perturb_percent = float(sys.argv[2])
all_edges = set()
all_nodes = set()

for line in el_file:
    node1, node2 = re.split('\s', line.strip())

    if node2 < node1:
        node1, node2 = node2, node1

    all_edges.add((node1, node2))
    all_nodes.add(node1)
    all_nodes.add(node2)

edge_list = list(all_edges)
node_list = list(all_nodes)
random.shuffle(edge_list)
random.shuffle(node_list)
num_edges = len(edge_list)
perturb_count = int(perturb_percent / 100 * num_edges)

# remove perturb_count many edges
edge_list = edge_list[:-perturb_count]
edge_set = set(edge_list)

def get_random_node(node_list):
    return node_list[random.randrange(len(node_list))]

def gen_erdos_renyi_edge(node_list):
    node1 = get_random_node(node_list)

    while True:
        node2 = get_random_node(node_list)

        if node2 != node1:
            break

    if node2 < node1:
        node1, node2 = node2, node1

    return (node1, node2)

while len(edge_set) < num_edges:
    edge = gen_erdos_renyi_edge(node_list)
    edge_set.add(edge)

edge_list = list(edge_set)
print('\n'.join([f'{node1} {node2}' for node1, node2 in edge_list]))
