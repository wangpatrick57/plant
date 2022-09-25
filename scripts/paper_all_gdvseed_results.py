#!/pkg/python/3.7.4/bin/python3
from all_helpers import *
import sys

notes_list = ['norm', 'a80', 'no1']
pairs = get_paper_all_pairs()
# start = pairs.index(('email_s0', 'email_s3'))
start = 0
pairs = pairs[start:]
all_all_results = get_all_all_results()

for gtag1, gtag2 in pairs:
    seeds, seed_metrics, extr_metrics = simplified_run_with_metrics(gtag1, gtag2, algo='bno', silent=True)
    extr_vol = extr_metrics[0]
    extr_ort_vol = extr_metrics[1]
    k = two_gtags_to_k(gtag1, gtag2)
    n = two_gtags_to_n(gtag1, gtag2)
    to_print = [f'{gtag1}-{gtag2}']

    for notes in notes_list:
        path = get_odv_ort_path(gtag1, gtag2, k, n, notes)

        try:
            odv_orts = read_in_odv_orts(path, include_score=False)
        except:
            print(f'{gtag1}-{gtag2} doesn\'t exist')
            continue

        odv_orts = odv_orts[:extr_vol]
        g1_to_g2 = get_g1_to_g2_orthologs(gtag1, gtag2)
        odv_orts_orts = get_orthopairs_list(odv_orts, g1_to_g2)
        to_print.append(len(odv_orts))
        to_print.append(len(odv_orts_orts))
    
    to_print.append(extr_vol)
    to_print.append(extr_ort_vol)
    print('\t'.join([str(e) for e in to_print]))
