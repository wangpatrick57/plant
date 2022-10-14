#!/pkg/python/3.7.4/bin/python3
from collections import defaultdict
from all_helpers import *

def get_seeds_deg_distr(seeds, adj_set, use_first_species=True):
    flattened_nodes = []

    for sid, nodes1, nodes2 in seeds:
        nodes_to_use = nodes1 if use_first_species else nodes2
        flattened_nodes.extend(nodes_to_use)

    return get_deg_distr(flattened_nodes, adj_set)

def get_alignments_deg_distr(alignments, adj_set, use_first_species=True):
    flattened_nodes = []

    for alignment in alignments:
        for node1, node2 in alignment:
            node_to_use = node1 if use_first_species else node2
            flattened_nodes.append(node_to_use)

    return get_deg_distr(flattened_nodes, adj_set)

def get_deg_distr(nodes, adj_set):
    deg_distr = defaultdict(int)

    for node in nodes:
        deg = len(adj_set[node])
        deg_distr[deg] += 1

    return deg_distr

def distr_to_str(distr, name):
    lines = []
    items = list(distr.items())
    items.sort(key=(lambda d: (-d[0], d[1])))
    lines.append(f'{name}\tcount')
    lines.extend([f'{val}\t{cnt}' for val, cnt in items])
    return '\n'.join(lines)

def print_distr(distr, name):
    print(distr_to_str(distr, name))

def print_deg_distr(deg_distr):
    print_distr(deg_distr, 'degree')

def get_alignment_nc(alignment, g1_to_g2_ort):
    from ortholog_helpers import is_ortholog

    alignment = get_injective_alignment(alignment)
    num_orts = 0

    for node1, node2 in alignment:
        if is_ortholog(node1, node2, g1_to_g2_ort):
            num_orts += 1

    return num_orts / len(alignment) if len(alignment) > 0 else 0

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

    weighted_squared_mean = 0 if total_nodes == 0 else weighted_squared_sum / total_nodes
    return weighted_squared_mean

def get_disjoint_alignments(alignments):
    # get alignments sorted from least to most common
    nodes1 = defaultdict(int)
    nodes2 = defaultdict(int)

    for alignment in alignments:
        for node1, node2 in alignment:
            nodes1[node1] += 1
            nodes2[node2] += 1

    aligns_by_commonality = []

    # this simple algorithm works assuming both networks have approximately equal sizes and densities, which they do
    # we'll just use arithmetic mean to keep it simple for now
    for alignment in alignments:
        commonality = sum([nodes1[node1] + nodes2[node2] for node1, node2 in alignment])
        aligns_by_commonality.append((alignment, commonality))

    aligns_by_commonality.sort(key=(lambda data : (data[1], data[0])))

    # add alignments from least to most common
    added_nodes1 = set()
    added_nodes2 = set()
    disjoint_alignments = []
    OVERLAP_THRESHOLD = 0.5

    for alignment, _ in aligns_by_commonality:
        overlapping_nodes1 = sum([1 if node1 in added_nodes1 else 0 for node1, _ in alignment])
        overlapping_nodes2 = sum([1 if node2 in added_nodes2 else 0 for _, node2 in alignment])
        overlap = (overlapping_nodes1 + overlapping_nodes2) / (2 * len(alignment))

        if overlap < OVERLAP_THRESHOLD:
            disjoint_alignments.append(alignment)

            for node1, node2 in alignment:
                added_nodes1.add(node1)
                added_nodes2.add(node2)

    return disjoint_alignments

def get_topofunc_acc(nc, s3):
    return (nc + s3) / 2

def get_size_acc_score(size, acc):
    return size * acc ** 2

def get_best_scoring_alignment(alignments, g1_to_g2_ort, adj_set1, adj_set2):
    best_alignment = None
    best_size = -1
    best_acc = -1
    best_score = -1
    
    for alignment in alignments:
        nc = get_alignment_nc(alignment, g1_to_g2_ort)
        s3 = get_s3(alignment, adj_set1, adj_set2)
        size = len(alignment)
        acc = get_topofunc_acc(nc, s3)
        score = get_size_acc_score(size, acc)
        
        if score > best_score:
            best_score = score
            best_size = size
            best_acc = acc
            best_alignment = alignment

    return (best_alignment, best_size, best_acc, best_score)

def get_size_acc_points(alignments, g1_to_g2_ort, adj_set1, adj_set2):
    all_size_acc_points = []
    
    for alignment in alignments:
        nc = get_alignment_nc(alignment, g1_to_g2_ort)
        s3 = get_s3(alignment, adj_set1, adj_set2)
        size = len(alignment)
        acc = get_topofunc_acc(nc, s3)
        all_size_acc_points.append((size, acc))

    all_size_acc_points.sort(key=(lambda data : (data[1], data[0])), reverse=True)
    size_acc_points = []
    max_size = -1

    for size, acc in all_size_acc_points:
        if size > max_size:
            size_acc_points.append((size, acc))
            max_size = size

    return size_acc_points

def get_topofunc_perfect_alignments(alignments, g1_to_g2_ort, adj_set1, adj_set2):
    tfp_aligns = []
    
    for alignment in alignments:
        nc = get_alignment_nc(alignment, g1_to_g2_ort)
        s3 = get_s3(alignment, adj_set1, adj_set2)

        if nc == 1 and s3 == 1:
            tfp_aligns.append(alignment)

    return tfp_aligns

def get_topofunc_perfect_seeds(seeds, g1_to_g2_ort, adj_set1, adj_set2):
    print(seeds[0])
    alignments = [[(node1, node2) for node1, node2 in zip(nodes1, nodes2)] for sid, nodes1, nodes2 in seeds]
    return get_topofunc_perfect_alignments(alignments, g1_to_g2_ort, adj_set1, adj_set2)

def get_avg_size(seeds):
    sizes = [len(nodes1) for gid, nodes1, nodes2 in seeds]
    return 0 if len(sizes) == 0 else sum(sizes) / len(sizes)

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
        # print(f'alignment has {len(alignment) - len(set(alignment))} duplicate pairs')
        pass
        
    if len(injective_alignment) != len(set(alignment)):
        # print(f'alignment has {len(set(alignment)) - len(injective_alignment)} non-injective pairs')
        pass
        
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

    s3 = num_common_edges / num_total_edges if num_total_edges > 0 else 0
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
