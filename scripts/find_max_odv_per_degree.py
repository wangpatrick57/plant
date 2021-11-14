import sys
from odv_helpers import *
from graph_helpers import *
from collections import defaultdict

species = sys.argv[1]
odv_num = int(sys.argv[2])

graph_fname = get_graph_fname_from_species(species)
graph_file = open(graph_fname, 'r')
odv_dir = ODVDirectory(get_odv_dir_path(species))
adj_set = read_adj_set(graph_file)

max_odv_per_degree = defaultdict(int)

for node in adj_set['P62260']:
    degree = len(adj_set[node])
    odv_val = odv_dir.get_odv(node).get_odv_val(odv_num)
    max_odv_per_degree[degree] = max(max_odv_per_degree[degree], odv_val)

print('\n'.join([f'{deg} {max_odv_val}' for deg, max_odv_val in max_odv_per_degree.items()]))
