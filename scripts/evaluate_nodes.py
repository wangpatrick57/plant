#!/bin/python3

import sys
from graph_helpers import *

species1 = sys.argv[1]
species2 = sys.argv[2]
nodes_file = open(sys.argv[3], 'r')

ORTHO_FILE = open('/home/wayne/src/bionets/SANA/Jurisica/IID/Orthologs.Uniprot.tsv', 'r')
s1_to_s2 = get_si_to_sj(species1, species2, ORTHO_FILE)

lines = 0
orthos = []


ortho_percent = 0 if lines == 0 else len(orthos) * 100 / lines
print(f'accuracy: {len(orthos)} / {lines} ()', file=sys.stderr)
print('\n'.join([f'{node1} {node2}' for node1, node2 in orthos]))
