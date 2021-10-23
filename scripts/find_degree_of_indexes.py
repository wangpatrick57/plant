import sys
from graph_helpers import *
from collections import defaultdict

species = sys.argv[1]
indexes_file = open(sys.argv[2], 'r')

graph_file = open(get_graph_fname_from_species(species), 'r')
adj_set = read_adj_set(graph_file)
deg_distr = defaultdict(int)

for line in indexes_file:
    line_split = line.strip().split(' ')
    nodes = line_split[1:]

    for node in nodes:
        node_deg = len(adj_set[node])
        deg_distr[node_deg] += 1

print('\n'.join([f'{deg} {count}' for deg, count in deg_distr.items()]))
