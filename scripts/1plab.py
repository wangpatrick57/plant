#!/bin/python3
from node_to_num_mapping import *
from file_helpers import *
from graph_helpers import *

graph_path = '/home/wangph1/plant/networks/temporal_slices/sxso_start+0_inter15000000.dmel'
mapping_path = '/home/wangph1/plant/data/static/sxso_start+0_i15M.n2n'

node_el = read_in_el('/home/wangph1/plant/networks/deepmatching/syeast0.dmel')
num_el = el_node_to_num('syeast0_shuf', node_el)
write_el_to_file(num_el, '/home/wangph1/plant/networks/deepmatching/syeast0_shuf.dmel')
