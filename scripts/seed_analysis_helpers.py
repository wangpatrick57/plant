#!/pkg/python/3.7.4/bin/python3
from collections import defaultdict
from all_helpers import *

def get_deg_distr(seeds, adj_set1, adj_set2):
    deg_distr = defaultdict(int)

    for gid, align1, align2 in seeds:
        for node in align1:
            deg = len(adj_set1[node])
            deg_distr[deg] += 1

        for node in align2:
            deg = len(adj_set2[node])
            deg_distr[deg] += 1

    return deg_distr

def print_deg_distr(deg_distr):
    items = list(deg_distr.items())
    items.sort(key=(lambda d: (-d[0], d[1])))
    print('degree\tcount')
    print('\n'.join([f'{deg}\t{cnt}' for deg, cnt in items]))

if __name__ == '__main__':
    gtag1 = 'syeast0'
    gtag2 = 'syeast05'
    g1_to_g2_orts = get_s1_to_s2_orthologs(gtag1, gtag2)
    adj_set1 = read_in_adj_set(get_gtag_graph_path(gtag1))
    adj_set2 = read_in_adj_set(get_gtag_graph_path(gtag2))
    seeds, _, _ = low_param_one_run(*get_gtag_run_info(gtag1, gtag2))
    orthoseeds = get_orthoseeds_list(seeds, g1_to_g2_orts)
    deg_distr = get_deg_distr(orthoseeds, adj_set1, adj_set2)
    print(len(seeds))
    print_deg_distr(deg_distr)
