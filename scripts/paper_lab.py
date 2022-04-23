#!/bin/python3
from graph_helpers import *
from temporal_graph_helpers import *
from file_helpers import *

graph_path = get_snap_graph_path('sx-stackoverflow.tel')
start_time = 1_217_567_877
interval = 15_000_000
delta = 5_000

while delta < interval:
    el = read_in_el_in_interval(graph_path, start_time + delta, start_time + delta + interval)
    file_path = f'/home/wangph1/plant/networks/temporal_slices/sxso_start+{delta}_inter{15_000_000}.el'
    write_el_to_file(el, file_path)
    delta *= 4
