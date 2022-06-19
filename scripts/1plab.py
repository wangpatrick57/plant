#!/pkg/python/3.7.4/bin/python3
import sys
from all_helpers import *

gtag1 = 'mouse'
gtag2 = 'rat'
k = two_gtags_to_k(gtag1, gtag2)
odv_dir1 = ODVDirectory(get_odv_path(gtag1, k))
odv_dir2 = ODVDirectory(get_odv_path(gtag2, k))
ODV.set_weights_vars(k)
nodes1 = ['P62259', 'Q61510', 'P12023', 'Q3UFB7', 'Q80V62']
nodes2 = ['P62260', 'D4A9N5', 'P08592', 'P35739', 'B5DF91']

for node1 in nodes1:
    for node2 in nodes2:
        odv1 = odv_dir1.get_odv(node1)
        odv2 = odv_dir2.get_odv(node2)
        sim = odv1.get_similarity(odv2)
        print(node1, node2, sim)
