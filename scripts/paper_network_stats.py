#!/pkg/python/3.7.4/bin/python3
from all_helpers import *

for gtag in get_paper_all_gtags():
    path = get_graph_path(gtag)
    el = read_in_el(path)
    nodes = el_to_nodes(el)
    real_name = gtag_to_real_name(gtag)
    print(f'{gtag}\t{len(el)}\t{len(nodes)}')
