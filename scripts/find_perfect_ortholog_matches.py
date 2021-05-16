import sys
from graph_helpers import *

species1 = sys.argv[1]
species2 = sys.argv[2]
seed_file = open(sys.argv[3], 'r')

ORTHO_FILE = open(f'/home/wayne/src/bionets/SANA/Jurisica/IID/Orthologs.Uniprot.tsv', 'r')

s1_to_s2 = get_si_to_sj(species1, species2, ORTHO_FILE)

for line in seed_file:
    patch_id, index1, index2 = line.strip().split()
    s1_nodes = index1.split(',')
    s2_nodes = index2.split(',')

    assert len(s1_nodes) == len(s2_nodes)

    num_not_matching = 0

    for s1n, s2n in zip(s1_nodes, s2_nodes):
        if s1n not in s1_to_s2 or s1_to_s2[s1n] != s2n:
            num_not_matching += 1

    if num_not_matching != 0:
        num_matching = len(s1_nodes) - num_not_matching
        print(line.strip() + ' ' + str(num_matching))
        # print(line.strip())
