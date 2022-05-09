#!/pkg/python/3.7.4/bin/python3
from temporal_graph_helpers import *
from graph_helpers import *
from file_helpers import *

tel = read_in_temporal_el('../networks/snap/math.tel')
els = get_tel_std_sections(tel)

for i, el in enumerate(els):
    write_el_to_file(el, f'../networks/snap/math{i}.el')
    graph_stats(el, f'otc{i}')
