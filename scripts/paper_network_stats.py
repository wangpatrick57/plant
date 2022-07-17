#!/pkg/python/3.7.4/bin/python3
from all_helpers import *

for gtag in get_paper_all_gtags()[10:]:
    if gtag in get_paper_tprl_snap():
        gtag = f'{gtag}_s0'

    path = get_graph_path(gtag)
    el = read_in_el(path)
    nodes = nodes_of_el(el)
    real_name = gtag_to_real_name(gtag)
    print(f'{gtag}\t{len(el)}\t{len(nodes)}')
