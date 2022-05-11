#!/pkg/python/3.7.4/bin/python3
import sys
from graph_helpers import *

graph_stats(read_in_el(get_snap_graph_path(sys.argv[1])))
# graph_stats(read_in_el(sys.argv[1]))
