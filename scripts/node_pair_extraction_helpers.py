#!/pkg/python/3.7.4/bin/python3
from collections import defaultdict
from file_helpers import *
from ortholog_helpers import *

def add_valid_edges(list_of_species_nodes, lines):
    num_edges = 0
    edges = set()
    for i in list_of_species_nodes:
        if(i[0] in lines and i[1] in lines):
            num_edges += 1
            edges.add((i[0], i[1]))
    return [edges, num_edges]

def bifurcate_mapping_into_dictionaries(preprocessed_nodes, left_node_frequencies, right_node_frequencies):
    counter = 0
    for i in preprocessed_nodes[0]:
        if i != "0" and preprocessed_nodes[1][counter] != "0":
            left_node_frequencies[i] += 1
            right_node_frequencies[preprocessed_nodes[1][counter]] += 1
            counter += 1
    return [left_node_frequencies, right_node_frequencies]

def remove_duplicate_mappings_from_dictionary(preprocessed_nodes, left_node_frequencies, right_node_frequencies):
    processed_list_of_nodes = list()
    counter = 0
    for i in preprocessed_nodes[0]:
        if i != "0" and preprocessed_nodes[1][counter] != "0":
            if not(left_node_frequencies[i] >= 1 or int(right_node_frequencies[preprocessed_nodes[1][counter]]) >= 1):
                processed_list_of_nodes.append((i, preprocessed_nodes[1][counter]))
        counter += 1
    return processed_list_of_nodes

def remove_dupes(list_of_nodes):

    left_node_frequencies = defaultdict(int) # Using Python's defaultdict
    right_node_frequencies = defaultdict(int) # Using Python's defaultdict
    final_list = list()

    left_node_frequencies = bifurcate_mapping_into_dictionaries(list_of_nodes, left_node_frequencies, right_node_frequencies)[0]
    right_node_frequencies = bifurcate_mapping_into_dictionaries(list_of_nodes, left_node_frequencies, right_node_frequencies)[1]
    
    final_list = remove_duplicate_mappings_from_dictionary(list_of_nodes, left_node_frequencies, right_node_frequencies)

    return final_list

def filtering_lists(name):

    processed_list = list()

    temporary_list = list_of_nodes_from_species(name)

    reformatted_nodes = []
    for i in temporary_list:
        reformatted_nodes.append(map(str, i))
    result = list(map(list, zip(*reformatted_nodes)))

    processed_list = remove_dupes(result)

    return processed_list

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
    orthopairs = get_orthopairs_list(node_pairs, SelfOrthos())
    print(f'{len(orthopairs)} / {len(node_pairs)}')
