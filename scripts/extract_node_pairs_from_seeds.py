#!/bin/python3

import sys
from collections import defaultdict

seeds_file = open(sys.argv[1], 'r')

def aug(node, n):
    return f'{n}_{node}'

def deaug(auged_node):
    return '_'.join(auged_node.split('_')[1:])

def add_to_voting(node1, node2):
    if node1 not in node_pair_voting:
        node_pair_voting[node1] = defaultdict(int)

    if node2 not in node_pair_voting:
        node_pair_voting[node2] = defaultdict(int)
    
    node_pair_voting[node1][node2] += 1
    node_pair_voting[node2][node1] += 1

def print_node_pair_voting():
    print('\n'.join([base + ': ' + ','.join(f'{node}:{count}' for node, count in votes.items()) for base, votes in node_pair_voting.items()]), file=sys.stderr)

def print_node_favorite_pairs():
    print('\n'.join([f'{base}: {favorites}' for base, favorites in node_favorite_pairs.items()]), file=sys.stderr)

def print_output_pairs():
    print('\n'.join([f'{deaug(node1)} {deaug(node2)}' for node1, node2 in output_pairs]))

# create node_pair_voting
node_pair_voting = dict()

for line in seeds_file:
    if line.strip() == '':
        continue

    graphlet_id, s1_index_str, s2_index_str = line.strip().split()
    s1_nodes = s1_index_str.split(',')
    s2_nodes = s2_index_str.split(',')

    for s1_node, s2_node in zip(s1_nodes, s2_nodes):
        add_to_voting(aug(s1_node, 1), aug(s2_node, 2))

# create node_favorite_pairs
node_favorite_pairs = defaultdict(set)

for base, votes in node_pair_voting.items():
    max_count = max([count for count in votes.values()])
    
    for node, count in votes.items():
        if count == max_count:
            node_favorite_pairs[base].add(node)

# get output pairs
output_pairs = set()

for node, favorites in node_favorite_pairs.items():
    for fav in favorites:
        if node == fav:
            exit('node equals fav')

        if node < fav: # only process in one direction to avoid duplicates
            if node in node_favorite_pairs[fav]:
                output_pairs.add((node, fav))

# debug
print_output_pairs()
