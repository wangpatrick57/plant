#!/pkg/python/3.7.4/bin/python3
from collections import defaultdict
from file_helpers import *
from ortholog_helpers import *

def extract_node_pairs(all_seeds_list):
    m2m_pairs = seeds_to_m2m(all_seeds_list)
    return extract_node_pairs_from_m2m(m2m_pairs)

# extracts node pairs from many2many alignments (.aln files)
def extract_node_pairs_from_m2m(m2m_pairs):
    node_pair_voting = create_node_pair_voting(m2m_pairs)
    node_favorite_pairs = create_node_favorite_pairs(node_pair_voting)
    output_pairs = create_output_pairs(node_favorite_pairs)
    return output_pairs    

def aug(node, n):
    return f'{n}_{node}'

def deaug(auged_node):
    return '_'.join(auged_node.split('_')[1:])

def print_output_pairs(output_pairs):
    print('\n'.join([f'{deaug(node1)} {deaug(node2)}' for node1, node2 in output_pairs]))

def create_node_pair_voting(m2m_pairs):
    def add_to_voting(node1, node2):
        if node1 not in node_pair_voting:
            node_pair_voting[node1] = defaultdict(int)

        if node2 not in node_pair_voting:
            node_pair_voting[node2] = defaultdict(int)

        node_pair_voting[node1][node2] += 1
        node_pair_voting[node2][node1] += 1

    node_pair_voting = dict()

    for s1_node, s2_node in m2m_pairs:
        add_to_voting(aug(s1_node, 1), aug(s2_node, 2))

    return node_pair_voting

def seeds_to_m2m(seeds):
    # has to be list, not set, because we want duplicates (they count towards the vote)
    m2m_pairs = list()

    for graphlet_id, s1_index, s2_index in seeds:
        for s1_node, s2_node in zip(s1_index, s2_index):
            m2m_pairs.append((s1_node, s2_node))

    return m2m_pairs

def create_node_favorite_pairs(node_pair_voting):
    node_favorite_pairs = defaultdict(set)

    for base, votes in node_pair_voting.items():
        max_count = max([count for count in votes.values()])

        for node, count in votes.items():
            if count == max_count:
                node_favorite_pairs[base].add(node)

    return node_favorite_pairs

def create_output_pairs(node_favorite_pairs):
    output_pairs = set()

    for node, favorites in node_favorite_pairs.items():
        for fav in favorites:
            if node == fav:
                exit('node equals fav')

            if node < fav: # only process in one direction to avoid duplicates
                if node in node_favorite_pairs[fav]:
                    output_pairs.add((deaug(node), deaug(fav)))

    return output_pairs

if __name__ == '__main__':
    path = get_data_path('mcl/alignments/syeast0-syeast25-5000.txt')
    print(path)
    m2m_pairs = read_in_slashes_m2m(path)
    node_pairs = extract_node_pairs_from_m2m(m2m_pairs)
    orthopairs = get_orthopairs_list(node_pairs, MarkedSelfOrthos())
    print(f'{len(orthopairs)} / {len(node_pairs)}')
