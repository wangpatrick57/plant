import sys
sys.path.insert(1, "/home/wangph1/plant/scripts")
from node_to_num_mapping import *
from ortholog_helpers import *

f = sys.argv[1]
species1 = sys.argv[2]
species2 = sys.argv[3]

seeds = open(f, "r")
convert1 = read_in_n2n(species1, False)
convert2 = read_in_n2n(species2, False)
nodepairs = []
seen = []
for line in seeds:
    nodes = [int(i) for i in line.strip().split('\t')]

    if (seen.__contains__(nodes[0]) or seen.__contains__(nodes[1])):
        print(f"INVALID: node {nodes[0]} or {nodes[1]} seen multiple times")
        continue
        # quit()

    seen.append(nodes[0])
    seen.append(nodes[1])
    nodepairs.append((convert1[nodes[0]], convert2[nodes[1]]))


orthos = get_orthopairs_list(nodepairs, get_s1_to_s2_orthologs(species1, species2))
acc = "%.3f"%(round(len(orthos)/len(nodepairs), 3))
volume = len(orthos)
print(f"accuracy: {acc}")
print(f"match volume: {volume}")

