#!/bin/python3
import sys
import random
from graph_helpers import *
from ortholog_helpers import *

def get_mapping_str(nodes):
    nodes = sorted(list(nodes))
    return '\n'.join([f'{node}\t{i}' for i, node in enumerate(nodes)])

def get_random_mapping_str(nodes):
    random_nodes = list(nodes)
    random.shuffle(random_nodes)
    return '\n'.join([f'{n}\t{rn}' for n, rn in zip(nodes, random_nodes)])

def output_random_mapping(graph_path, mapping_path):
    nodes = read_in_nodes(graph_path)
    fout = open(mapping_path, 'w')
    fout.write(get_random_mapping_str(nodes))
    fout.close()

def output_mapping_for_species(species):
    nodes = read_in_nodes(get_graph_path(species))
    fout = open(get_n2n_fname_for_species(species), 'w')
    fout.write(get_mapping_str(nodes))
    fout.close()

def output_mapping_for_all_species():
    for species in all_species():
        output_mapping_for_species(species)

def get_n2n_fname_for_species(species):
    return f'/home/wangph1/plant/data/static/{species}.n2n'

def read_in_n2n(species, forward=True, convert_to_int=True):
    f = open(get_n2n_fname_for_species(species), 'r')
    n2n = dict()
    
    for line in f:
        node, num = line.strip().split('\t')

        if convert_to_int:
            num = int(num)

        if forward:
            k = node
            v = num
        else:
            k = num
            v = node

        if k in n2n:
            print('ERROR: DUPLICATE KEY', file=sys.stderr)
            quit()

        n2n[k] = v

    f.close()
    return n2n

def el_node_to_num(species, node_el):
    node_to_num = read_in_n2n(species, forward=True)
    num_el = []

    for node1, node2 in node_el:
        num_el.append((node_to_num[node1], node_to_num[node2]))

    return num_el

def get_num_s1_to_s2_orthologs(species1, species2):
    s1_to_s2_orthologs = get_s1_to_s2_orthologs(species1, species2)
    num_s1_to_s2_orthologs = dict()
    s1_n2n = read_in_n2n(species1)
    s2_n2n = read_in_n2n(species2)

    for s1_node, s2_node in s1_to_s2_orthologs.items():
        if s1_node in s1_n2n and s2_node in s2_n2n:
            num_s1_to_s2_orthologs[str(s1_n2n[s1_node])] = str(s2_n2n[s2_node])

    return num_s1_to_s2_orthologs

if __name__ == '__main__':
    for species in ['syeast0', 'syeast05', 'syeast10', 'syeast15', 'syeast20', 'syeast25']:
        output_mapping_for_species(species)
