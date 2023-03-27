#!/bin/python3
from all_helpers import *
from run_sag import get_sag_alignment_path

tprl_base_gtags = ['reddit', 'sxso', 'math', 'super', 'ubuntu', 'wiki', 'email', 'college', 'otc', 'alpha']
sag_all_results = read_in_pair_sns_results(get_results_path('sag_all'))
print(',' + ','.join([f'{gtag}_s0' for gtag in tprl_base_gtags]))

for s in [1, 3, 5]:
    print(f'{s}', end=',')
    
    for base_gtag in tprl_base_gtags:
        gtag1 = f'{base_gtag}_s0'
        gtag2 = f'{base_gtag}_s{s}'
        size, nc, s3 = sag_all_results[f'{gtag1}-{gtag2}']
        val = size * nc ** 2 * s3 ** 2
        print(f'{val}', end=',')

    print()
