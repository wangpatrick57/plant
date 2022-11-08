#!/bin/python3
# this is the simulated annealing algorithm that merges in rounds, not the one that grows an alignment
from all_helpers import *
import sys
# read in seeds
# in every round, every single alignment from the previous round has to be used
# every alignment is then aligned with some other previous alignment
# move: take one alignment and make it pick a new partner. if that partner's already being used, perform a swap
# energy: total number of nodes which are above the threshold
# for each alignment, store its numerator and denominator (assume s3=1 for now)

if __name__ == '__main__':
    gtag1 = sys.argv[1]
    gtag2 = sys.argv[2]
    algo = sys.argv[3]
    adj_set1 = read_in_adj_set(get_graph_path(gtag1))
    adj_set2 = read_in_adj_set(get_graph_path(gtag2))
    seeds_path = get_seeds_path(gtag1, gtag2, algo=algo, prox=1, target_num_matching=1)
    seeds = read_in_seeds(seeds_path)
    print(len(seeds))
