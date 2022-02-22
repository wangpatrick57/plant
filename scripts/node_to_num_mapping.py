#!/bin/python3
import sys
from graph_helpers import *

def get_mapping_str(nodes):
    nodes = sorted(list(nodes))
    return '\n'.join([f'{node}\t{i}' for i, node in enumerate(nodes)])

def output_mapping_for_species(species):
    fin = open(get_graph_fname_from_species(species))
    nodes = read_nodes(fin)
    fin.close()
    fout = open(get_n2n_fname_for_species(species), 'w')
    fout.write(get_mapping_str(nodes))
    fout.close()

def output_mapping_for_all_species():
    for species in all_species():
        output_mapping_for_species(species)

def get_n2n_fname_for_species(species):
    return f'/home/wangph1/plant/data/static/{species}.n2n'

def read_in_n2n(species, forward=True):
    f = open(get_n2n_fname_for_species(species), 'r')
    n2n = dict()
    
    for line in f:
        node, num = line.strip().split('\t')
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

def el_node_to_num(node_el):
    node_to_num = read_in_n2n(node_el, forward=True)
    num_el = []

    for node1, node2 in node_el:
        num_el.append((node_to_num[node1], node_to_num[node2]))

    return num_el

if __name__ == '__main__':
    print(read_in_n2n('rat', forward=False))
