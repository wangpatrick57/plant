#!/bin/python3
from all_helpers import *
from run_sag import get_sag_alignment_path

print_table = True
sep = ' & ' if print_table else '\t'
species_order = ['cat', 'cow', 'dog', 'guineapig', 'rat', 'pig', 'mouse', 'rabbit', 'horse', 'sheep', 'human']
sag_all_results = read_in_pair_sns_results(get_results_path('sag_all'))
mcl_nc_frontier_results = read_in_frontier_results(get_results_path('mcl_nc_frontier'))

if print_table:
    print('\\toprule')
    
print('.' + sep + sep.join(species_order), end='')

if print_table:
    print('\\\\')
else:
    print()

if print_table:
    print('\\midrule')

for gtag1 in species_order:
    print(f'{gtag1}', end=sep)

    for gtag2 in species_order:
        if gtag1 == gtag2:
            print('.', end=sep)
        else:
            pair = f'{min(gtag1, gtag2)}-{max(gtag1, gtag2)}'
            nc_frontier = mcl_nc_frontier_results[pair]
            frontier_vals = [int(size) * float(nc) ** 2 * float(nc) for size, nc in nc_frontier] # using sqrt(nc) as an approximate value for s3. that's why we did * nc at the end, it represents ~(s3 ** 2)

            if len(frontier_vals) == 0:
                mcl_val = 1000000
                print(f'no frontier for pair {pair}', file=sys.stderr)
            else:
                mcl_val = max(frontier_vals)
                
            blant_size, blant_nc, blant_s3 = sag_all_results[pair]
            blant_val = blant_size * blant_nc ** 2 * blant_s3 ** 2

            if print_table:
                print(f'{blant_val / mcl_val : .1f}x', end=sep)
            else:
                print(f'{blant_val / mcl_val}', end=sep)

    if print_table:
        print('\\\\')
    else:
        print()

if print_table:
    print('\\bottomrule')
