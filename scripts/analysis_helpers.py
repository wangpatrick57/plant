#!/pkg/python/3.7.4/bin/python3
from collections import defaultdict
from all_helpers import *

def get_deg_distr(nodes, adj_set):
    deg_distr = defaultdict(int)

    for node in nodes:
        deg = len(adj_set[node])
        deg_distr[deg] += 1

    return deg_distr

def deg_distr_to_str(deg_distr):
    lines = []
    items = list(deg_distr.items())
    items.sort(key=(lambda d: (-d[0], d[1])))
    lines.append('degree\tcount')
    lines.extend([f'{deg}\t{cnt}' for deg, cnt in items])
    return '\n'.join(lines)

def print_deg_distr(deg_distr):
    print(deg_distr_to_str(deg_distr))

def get_seed_nc(seeds, g1_to_g2_ort):
    from ortholog_helpers import is_ortholog

    total_nodes = 0
    weighted_squared_sum = 0

    for gid, nodes1, nodes2 in seeds:
        assert len(nodes1) == len(nodes2), print(gid, nodes1, nodes2, sep='\n')
        seed_size = len(nodes1)
        total_nodes += seed_size
        seed_num_ort = 0
        
        for node1, node2 in zip(nodes1, nodes2):
            if is_ortholog(node1, node2, g1_to_g2_ort):
                seed_num_ort += 1

        weighted_squared_sum += seed_num_ort ** 2 / seed_size # simplified from size * ort ^ 2 / size ^ 2

    weighted_squared_mean = weighted_squared_sum / total_nodes
    return weighted_squared_mean

def get_avg_size(seeds):
    sizes = [len(nodes1) for gid, nodes1, nodes2 in seeds]
    return sum(sizes) / len(sizes)

def get_alignment_repeats(alignment):
    saw1 = set()
    saw2 = set()
    num_repeats1 = 0
    num_repeats2 = 0

    for node1, node2 in alignment:
        if node1 in saw1:
            num_repeats1 += 1
        else:
            saw1.add(node1)

        if node2 in saw2:
            num_repeats2 += 1
        else:
            saw2.add(node2)

    return (num_repeats1, num_repeats2)

def get_injective_alignment(alignment):
    added1 = set()
    added2 = set()
    injective_alignment = []

    # one notable edge case is that if you have 01 02 12 it'll take 01 and 12. it skips over 02 even though it's the first appearance of 2 on the right side, because 02 has a 0 on the left side
    # in other words, added is the nodes in the order of being added, not in the order of being seen
    for node1, node2 in alignment:
        if node1 in added1:
            continue

        if node2 in added2:
            continue

        # we only add to saw when we add both nodes to the actual alignment
        injective_alignment.append((node1, node2))
        added1.add(node1)
        added2.add(node2)

    if len(set(alignment)) != len(alignment):
        print(f'alignment has {len(alignment) - len(set(alignment))} duplicate pairs')
        
    if len(injective_alignment) != len(set(alignment)):
        print(f'alignment has {len(set(alignment)) - len(injective_alignment)} non-injective pairs')
        
    return injective_alignment

def alignment_to_mapping(alignment):
    # if there are a lot of repeats in alignmcl, we'll also need to remove them with a separate function
    # this one does not remove repeats perfectly since there still could be repeats in the values
    alignment = get_injective_alignment(alignment)
    align_mapping = dict()
    num_repeats = 0

    for node1, node2 in alignment:
        align_mapping[node1] = node2

    return align_mapping

def get_s3(alignment, adj_set1, adj_set2):
    align_mapping = alignment_to_mapping(alignment)

    num_total_edges = 0
    num_common_edges = 0
    nodes1 = list(align_mapping.keys())

    for i in range(len(nodes1)):
        for j in range(i + 1, len(nodes1)):
            edge1 = (nodes1[i], nodes1[j])
            edge2 = (align_mapping[edge1[0]], align_mapping[edge1[1]])
            # my adj_sets are symmetric by convention
            edge1_exists = edge1[1] in adj_set1[edge1[0]]
            edge2_exists = edge2[1] in adj_set2[edge2[0]]

            if edge1_exists and edge2_exists:
                num_common_edges += 1

            if edge1_exists or edge2_exists:
                num_total_edges += 1

    s3 = num_common_edges / num_total_edges
    return s3

if __name__ == '__main__':
    gtag1 = 'syeast0'
    gtag2 = 'syeast05'
    g1_to_g2_orts = get_s1_to_s2_orthologs(gtag1, gtag2)
    adj_set1 = read_in_adj_set(get_graph_path(gtag1))
    adj_set2 = read_in_adj_set(get_graph_path(gtag2))
    seeds, _, _ = raw_full_low_param_run(*get_gtag_run_info(gtag1, gtag2))
    orthoseeds = get_orthoseeds_list(seeds, g1_to_g2_orts)
    deg_distr = get_deg_distr(orthoseeds, adj_set1, adj_set2)
    print(len(seeds))
    print_deg_distr(deg_distr)
