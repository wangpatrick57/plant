#!/bin/python3
import sys
from graph_helpers import *
from collections import defaultdict

species = sys.argv[1]
orthoseeds_file = open(sys.argv[2], 'r')
one_or_two = sys.argv[3]
assert one_or_two == '1' or one_or_two == '2'
graph_file = open(get_graph_fname_from_species(species), 'r')
adj_set = read_adj_set(graph_file)
deg_distr = defaultdict(int)

for line in orthoseeds_file:
    graphlet_id, graphlet1, graphlet2 = line.strip().split('\t')

    if one_or_two == '1':
        graphlet = graphlet1
    elif one_or_two == '2':
        graphlet = graphlet2

    for node in graphlet.split(','):
        node_deg = len(adj_set[node])
        deg_distr[node_deg] += 1

print('\n'.join([f'{deg} {count}' for deg, count in deg_distr.items()]))
