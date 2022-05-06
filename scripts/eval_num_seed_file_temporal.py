#!/bin/python3
import sys
from node_to_num_mapping import *
from ortholog_helpers import *
from graph_helpers import *

f = sys.argv[1]
ortho = sys.argv[2]

if ortho == 'time_shuf':
    s1_to_s2_orthologs = read_in_n2n('sxso_start+0_i15M', forward=False, convert_to_int=False)
elif ortho[0:3] == 'iid':
    species1 = ortho.split('_')[1]
    species2 = ortho.split('_')[2]
    s1_to_s2_orthologs = get_s1_to_s2_orthologs(species1, species2)
elif ortho == 'self':
    s1_to_s2_orthologs = SelfOrthos()
else:
    raise AssertionError('need to specify valid ortho string')

seeds = read_in_seeds(f)
orthos = get_orthopairs_list(seeds, s1_to_s2_orthologs)
acc = "%.3f"%(round(len(orthos)/len(seeds), 3))
volume = len(orthos)
print(f"accuracy: {acc}")
print(f"match volume: {volume}")
