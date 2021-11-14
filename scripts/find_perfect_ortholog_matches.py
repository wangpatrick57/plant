import sys
from graph_helpers import *

species1 = sys.argv[1]
species2 = sys.argv[2]
seed_file = open(sys.argv[3], 'r')

MATCH_THRESHOLD = 7
ORTHO_FILE = open(f'/home/wayne/src/bionets/SANA/Jurisica/IID/Orthologs.Uniprot.tsv', 'r')

s1_to_s2 = get_si_to_sj(species1, species2, ORTHO_FILE)
num_orthoseeds = 0
num_allseeds = 0

for line in seed_file:
    patch_id, index1, index2 = line.strip().split()
    s1_nodes = index1.split(',')
    s2_nodes = index2.split(',')

    assert len(s1_nodes) == len(s2_nodes)

    num_matching = 0

    for s1n, s2n in zip(s1_nodes, s2_nodes):
        if s1n in s1_to_s2 and s1_to_s2[s1n] == s2n:
            num_matching += 1

    if num_matching >= MATCH_THRESHOLD:
        print(line.strip() + ' ' + str(num_matching))
        num_orthoseeds += 1

    num_allseeds += 1

percent = 0 if num_allseeds == 0 else num_orthoseeds * 100 / num_allseeds
print(f'for {MATCH_THRESHOLD} matching, there are {num_orthoseeds} / {num_allseeds} orthoseeds, representing {percent}%', file=sys.stderr)
