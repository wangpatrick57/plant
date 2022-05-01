#!/bin/python3
import sys
from general_helpers import *
from node_to_num_mapping import *

def remove_self_loops(el):
    out_el = []

    for node1, node2 in el:
        if node1 != node2:
            out_el.append((node1, node2))

    return out_el

def directify(el):
    out_el = []

    for node1, node2 in el:
        out_el.append((node1, node2))
        out_el.append((node2, node1))

    return out_el

def bel2dmel_with_n2n(el):
    # TODO
    num_el = el_node_to_num(species, el)
    no_self_loops_el = remove_self_loops(num_el)
    directed_el = directify(no_self_loops_el)
    deduped_el = list(set(directed_el))
    sorted_el = sorted(deduped_el)
    return sorted_el

def bel2dmel(num_el):
    no_self_loops_el = remove_self_loops(num_el)
    directed_el = directify(no_self_loops_el)
    deduped_el = list(set(directed_el))
    sorted_el = sorted(deduped_el)
    return sorted_el

if __name__ == '__main__':
    species = sys.argv[1] if len(sys.argv) > 1 else 'mouse'
    dmel = bel2dmel(get_graph_path(species))
    outf = open(f'/home/wangph1/plant/networks/deepmatching/{species_to_full_name(species)}.dmel', 'w')
    outf.write('\n'.join(f'{node1}\t{node2}' for node1, node2 in dmel))
    outf.close()
