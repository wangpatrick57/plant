#!/bin/python3
from all_helpers import *
from run_sag import get_sag_alignment_path

species_order = ['cat', 'cow', 'dog', 'guineapig', 'rat', 'pig', 'mouse', 'rabbit', 'horse', 'sheep', 'human']
sag_all_results = read_in_pair_sns_results(get_results_path('sag_all'))
print(',' + ','.join(species_order))

for gtag1 in species_order:
    print(f'{gtag1}', end=',')

    for gtag2 in species_order:
        if gtag1 == gtag2:
            print('-', end=',')
        else:
            size, nc, s3 = sag_all_results[f'{min(gtag1, gtag2)}-{max(gtag1, gtag2)}']
            val = size * nc ** 2 * s3 ** 2
            print(f'{val}', end=',')

    print()
