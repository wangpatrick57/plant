#!/pkg/python/3.7.4/bin/python3
from graph_helpers import *
from file_helpers import *

base = 'gnutellafour'
el = read_in_el(get_snap_graph_path(f'{base}.el'))
soft5v1_el = soften_el(el, 0.05)
soft5v2_el = soften_el(el, 0.05)
soft10v1_el = soften_el(el, 0.1)
soft10v2_el = soften_el(el, 0.1)

for this_el in [soft5v1_el, soft5v2_el, soft10v1_el, soft10v2_el]:
    graph_stats(this_el, base)

write_el_to_file(soft5v1_el, get_snap_graph_path(f'{base}_5v1.el'))
write_el_to_file(soft5v2_el, get_snap_graph_path(f'{base}_5v2.el'))
write_el_to_file(soft10v1_el, get_snap_graph_path(f'{base}_10v1.el'))
write_el_to_file(soft10v2_el, get_snap_graph_path(f'{base}_10v2.el'))
