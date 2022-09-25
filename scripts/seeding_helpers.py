#!/pkg/python/3.7.4/bin/python3
from all_helpers import *

def add_max_degree_to_pairs(pairs, adj_set1, adj_set2):
    mdpairs = []

    for node1, node2 in pairs:
        max_deg = max(len(adj_set1[node1]), len(adj_set2[node2]))
        mdpairs.append((node1, node2, max_deg))

    mdpairs.sort(key=(lambda data: (-data[2], data[0], data[1])))
    return mdpairs

def get_max_degree_pairs_str(mdpairs):
    return '\n'.join(f'{node1}\t{node2}\t{max_deg}' for node1, node2, max_deg in mdpairs)

if __name__ == '__main__':
    gtag1 = 'syeast0'
    gtag2 = 'syeast15'
    adj_set1 = read_in_adj_set(get_graph_path(gtag1))
    adj_set2 = read_in_adj_set(get_graph_path(gtag2))
    seeds, seed_metrics, extr_metrics = raw_full_low_param_run(*get_gtag_run_info(gtag1, gtag2, s1_alph=True, s2_alph=True, algo='stairs'))
    pairs = extract_node_pairs(seeds)
    mdpairs = add_max_degree_to_pairs(pairs, adj_set1, adj_set2)
    write_to_file(get_max_degree_pairs_str(mdpairs), f'{gtag1}-{gtag2}-pairswdeg.out')
        
