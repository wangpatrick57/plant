#!/pkg/python/3.7.4/bin/python3
from all_helpers import *

path = get_fake_ort_path('mouse-rat-k4-n1500-a80', 'ort')
nodes = odv_ort_file_to_nodes(path, True)
adj_set = read_in_adj_set(get_graph_path('mouse'))
deg_distr = get_deg_distr(nodes, adj_set)
write_to_file(deg_distr_to_str(deg_distr), 'temp')
