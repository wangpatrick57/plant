#!/pkg/python/3.7.4/bin/python3
from all_helpers import *

n = 10
path = get_base_graph_path(f'syeast/syeast{n}')
el = read_in_el(path)
out_path = get_base_graph_path(f'syeast/syeast{n}_marked')

with open(out_path, 'w') as f:
    for node1, node2 in el:
        node1 = f'sy{n}_{node1}'
        node2 = f'sy{n}_{node2}'
        f.write(f'{node1}\t{node2}\n')
