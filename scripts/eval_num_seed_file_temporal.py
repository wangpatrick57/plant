#!/bin/python3
import sys
from node_to_num_mapping import *
from ortholog_helpers import *

f = sys.argv[1]

seeds = open(f, "r")
nodepairs = []
seen = []
for line in seeds:
    nodes = [i for i in line.strip().split('\t')]

    # if (seen.__contains__(nodes[0]) or seen.__contains__(nodes[1])):
        # print(f"INVALID: node {nodes[0]} or {nodes[1]} seen multiple times")
        # continue
        # quit()

    seen.append(nodes[0])
    seen.append(nodes[1])
    nodepairs.append((int(nodes[0]), nodes[1]))

s1_to_s2_orthologs = read_in_n2n('sxso_start+0_i15M', forward=False)
print(s1_to_s2_orthologs)
orthos = get_orthopairs_list(nodepairs, s1_to_s2_orthologs)
acc = "%.3f"%(round(len(orthos)/len(nodepairs), 3))
volume = len(orthos)
print(f"accuracy: {acc}")
print(f"match volume: {volume}")
