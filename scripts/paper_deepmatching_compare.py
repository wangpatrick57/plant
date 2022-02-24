#!/bin/python3
from graph_helpers import *
from full_algorithm_helpers import *

def get_syeast_fname(n):
    return f'/home/wangph1/BLANT/networks/syeast{n}/syeast{n}.el'

def eval_results(results_fname):
    results_file = open(results_fname, 'r')
    node_pairs = []

    for line in results_file:
        node1, node2 = re.split('[\s\t]', line.strip())
        node_pairs.add((node1, node2))

    results_file.close()
    node_pairs = list(set(node_pairs))
    return calc_acc_and_vol(node_pairs)

def calc_acc_and_vol(node_pairs):
    match_vol = 0

    for node1, node2 in node_pairs:
        if node1 == node2:
            match_vol += 1

    return (match_vol / len(node_pairs), match_vol)

def find_seeds(k, species1, species2, s1_index_path, s2_index_path, s1_odv_path=None, s2_odv_path=None, settings=SeedingAlgorithmSettings(), print_progress=False):
    pass

if __name__ == '__main__':
    all_nodes = set()

    for i in [0, 5, 10, 15, 20, 25]:
        results_fname = f'/home/wangph1/plant/data/deepmatching/bl-sy{i}-sy{i}.out'
        acc, match_vol = eval_results(results_fname)
        print(f'acc={acc}, match_vol={match_vol}')
