#!/pkg/python/3.7.4/bin/python3
import sys
from graph_helpers import *
from blant import *

# adv_num=0 is the edge between the top two nodes
def get_adversarial_edge(edge_set, sorted_nodes, rm_num):
    adv_num = 0

    for r in range(len(sorted_nodes)):
        for c in range(0, r):
            node1 = sorted_nodes[r]
            node2 = sorted_nodes[c]

            if in_edge_set(node1, node2, edge_set):
                # just found edge of curr adv_num
                if adv_num == rm_num:
                    return (node1, node2)
                
                # inc adv_num for next time
                adv_num += 1

if __name__ == '__main__':
    gtag = sys.argv[1]
    path = get_graph_path(gtag)
    el = read_in_el(path)
    edge_set = set(el)
    adj_set = read_in_adj_set(path)
    nodes = read_in_nodes(path)
    heurs = get_deg_heurs(nodes, adj_set)
    sorted_nodes = blant_sorted(nodes, heurs, True)

    for i in range(7):
        print(get_adversarial_edge(edge_set, sorted_nodes, i))
