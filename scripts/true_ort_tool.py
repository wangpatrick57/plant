#!/pkg/python/3.7.4/bin/python3
import sys
import random
from all_helpers import *

gtag1 = sys.argv[1]
gtag2 = sys.argv[2]
notes = sys.argv[3]
mark1 = gtag_to_mark(gtag1)
mark2 = gtag_to_mark(gtag2)
k = two_gtags_to_k(gtag1, gtag2)
n = two_gtags_to_n(gtag1, gtag2)
ort = get_g1_to_g2_orthologs(gtag1, gtag2)
s = ''

for node1, node2 in ort.items():
    marked_node1 = f'{mark1}_{node1}'
    marked_node2 = f'{mark2}_{node2}'

    if notes == 'true':
        score = 1.0
    else:
        score = random.uniform(0.6, 1.0)

    s += f'{marked_node1}\t{marked_node2}\t{score}\n'

write_to_file(s, get_data_path(f'mcl/fake_ort/{gtag1}-{gtag2}-k{k}-n{n}-{notes}.ort'))
