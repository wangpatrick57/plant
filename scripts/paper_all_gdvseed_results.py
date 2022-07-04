#!/pkg/python/3.7.4/bin/python3
from all_helpers import *
import sys

notes = sys.argv[1]
pairs = get_paper_all_pairs()
# start = pairs.index(('email_s0', 'email_s3'))
start = 0
pairs = pairs[start:]
all_all_results = get_all_all_results()

for gtag1, gtag2 in pairs:
    k = two_gtags_to_k(gtag1, gtag2)
    n = two_gtags_to_n(gtag1, gtag2)
    path = get_odv_ort_path(gtag1, gtag2, k, n, notes)

    try:
        odv_orts = read_in_odv_orts(path, include_score=False)
    except:
        print(f'{gtag1}-{gtag2} doesn\'t exist')
        continue

    g1_to_g2 = get_g1_to_g2_orthologs(gtag1, gtag2)
    odv_orts_orts = get_orthopairs_list(odv_orts, g1_to_g2)
    print(len(odv_orts), len(odv_orts_orts), sep='\t')
