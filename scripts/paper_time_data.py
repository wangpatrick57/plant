#!/pkg/python/3.7.4/bin/python3
from all_helpers import *

for gtag in get_paper_all_gtags(False):
    idx_path = get_index_path(gtag)
    graph_path = get_graph_path(gtag)
    nodes = read_in_nodes(graph_path)
    idx_vol, idx_time = extract_index_metrics(idx_path)
    print(gtag, len(nodes), idx_time)
