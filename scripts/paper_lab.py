#!/bin/python3
from graph_helpers import *
from temporal_graph_helpers import *

graph_path = get_snap_graph_path('sx-stackoverflow.tel')
get_edge_limit_node_edge_ratios(graph_path, 1217567877, 5000000, 10, 300000)
