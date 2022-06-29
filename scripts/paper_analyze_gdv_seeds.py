#!/pkg/python/3.7.4/bin/python3
from all_helpers import *
import sys

GDV_N = 3333
gtag1 = sys.argv[1]
gtag2 = sys.argv[2]
notes = sys.argv[3]
n = int(sys.argv[4])
k = two_gtags_to_k(gtag1, gtag2)
odv_ort_path = get_odv_ort_path(gtag1, gtag2, k, GDV_N, notes=notes)
odv_orts = read_in_odv_orts(odv_ort_path)
top_n_seeds = [(node1, node2) for node1, node2, score in odv_orts[:n]]
g1_to_g2_orthologs = get_g1_to_g2_orthologs(gtag1, gtag2)
ort_seeds = get_orthopairs_list(top_n_seeds, g1_to_g2_orthologs)
print(f'{len(ort_seeds)} / {len(top_n_seeds)}')
