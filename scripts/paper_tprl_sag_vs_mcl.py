#!/bin/python3
from all_helpers import *
from run_sag import get_sag_alignment_path

print_table = True
sep = ' & ' if print_table else '\t'
tprl_base_gtags = ['reddit', 'sxso', 'math', 'super', 'ubuntu', 'wiki', 'email', 'college', 'otc', 'alpha']
sag_all_results = read_in_pair_sns_results(get_results_path('sag_all'))
mcl_nc_frontier_results = read_in_frontier_results(get_results_path('mcl_nc_frontier'))

if print_table:
    print('\\toprule')

print('.' + sep + sep.join(tprl_base_gtags), end='')

if print_table:
    print('\\\\')
else:
    print()

if print_table:
    print('\\midrule')

for s in [1, 3, 5]:
    print(f'{s}', end=sep)
    
    for base_gtag in tprl_base_gtags:
        gtag1 = f'{base_gtag}_s0'
        gtag2 = f'{base_gtag}_s{s}'
        pair = f'{gtag1}-{gtag2}'
        nc_frontier = mcl_nc_frontier_results[pair]
        frontier_vals = [int(size) * float(nc) ** 2 * float(nc) for size, nc in nc_frontier] # using sqrt(nc) as an approximate value for s3. that's why we did * nc at the end, it represents ~(s3 ** 2)
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
