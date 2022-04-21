#!/bin/python3
from graph_helpers import *
from temporal_graph_helpers import *

tel = read_in_temporal_el(get_snap_graph_path('sx-stackoverflow.tel'))
map_density_over_time(tel)
