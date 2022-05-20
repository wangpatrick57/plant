#!/pkg/python/3.7.4/bin/python3
from graph_helpers import *

def blant_sorted(nodes, heurs, alph):
    nwhs = list(zip(nodes, heurs))

    if alph:
        nwhs.sort(key=(lambda nwh: (-nwh[1], nwh[0])))
    else:
        nwhs.sort(key=(lambda nwh: (nwh[1], nwh[0])), reverse=True)

    return [node for node, heur in nwhs]

def run_blant(el, lDEG=2, alph=True):
    pass

if __name__ == '__main__':
    path = get_gtag_graph_path('syeast0')
    el = read_in_el(path)
    run_blant(el)

    nodes = ['a', 'b', 'c', 'd', 'e']
    heurs = [1, 2, 1, 5, 1]
    print(blant_sorted(nodes, heurs, False))
