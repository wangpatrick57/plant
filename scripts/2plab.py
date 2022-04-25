#!/bin/python3
from graph_helpers import *

base_dir = '/home/wangph1/plant/networks/temporal_slices'

deltas = [0]

foo = 5000

while foo <= 5120000:
    deltas.append(foo)
    foo *= 4

for delta in deltas:
    graph_path = f'{base_dir}/sxso_start+{delta}_inter15000000.el'
    el = read_in_el(graph_path)
    graph_stats(el, name=f'delta={delta}')
