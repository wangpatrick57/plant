import sys
import bv2el

def get_el_from_sparsegraph(sparsegraph):
    nv, ne, starts, degrees, neighs = sparsegraph.split(';')

    nv = int(nv)
    ne = int(ne)
    starts = [int(e) for e in starts.split(',')]
    degrees = [int(e) for e in degrees.split(',')]
    neighs = [int(e) for e in neighs.split(',')]
    assert(len(starts) == nv)
    assert(len(degrees) == nv)
    assert(len(neighs) == ne)
    el = []

    for base_node in range(nv):
        this_start = starts[base_node]
        this_end = this_start + degrees[base_node]

        for neigh_node in neighs[this_start:this_end]:
            el.append((base_node, neigh_node))

    return el

if __name__ == '__main__':
    sparsegraph = sys.argv[1]
    bv2el.print_el(get_el_from_sparsegraph(sparsegraph))
