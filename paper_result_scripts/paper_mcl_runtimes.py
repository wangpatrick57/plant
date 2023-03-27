#!/bin/python3
from all_helpers import *

notes = 'no1'

for gtag1, gtag2 in get_paper_all_pairs():
    n = two_gtags_to_n(gtag1, gtag2)
    avg_n = (gtag_to_n(gtag1) + gtag_to_n(gtag2)) / 2
    k = two_gtags_to_k(gtag1, gtag2)
    out_path, ag_path, time_path = get_mcl_paths(gtag1, gtag2, k, n, notes=notes)

    with open(time_path, 'r') as time_file:
        lines = time_file.readlines()
        time_line = lines[1]
        after_m = time_line.split('m')[1]
        time_str = after_m.split('s')[0]
        mcl_time = float(time_str)
    
    print(f'{gtag1}-{gtag2}', avg_n, mcl_time, sep='\t')
