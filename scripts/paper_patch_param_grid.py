#!/pkg/python/3.7.4/bin/python3
import sys
from full_algorithm_helpers import *
from index_helpers import *
from graph_helpers import *
from ortholog_helpers import *

gtag1 = sys.argv[1]
gtag2 = sys.argv[2]
algo = 'bno'
lDEG = 2

extr_nc = []
extr_vol = []

for prox in [1, 2, 3, 4, 5, 8, 12, 15, 20, 25, 30]:
    extr_nc.append([])
    extr_vol.append([])

    for target_num_matching in range(1, 8):
        seeds, seed_metrics, extr_metrics = raw_full_low_param_run(*get_gtag_run_info(gtag1, gtag2, g1_alph=True, g2_alph=True, algo=algo, lDEG=lDEG), prox=-prox, target_num_matching=-target_num_matching)
        extr_vol[-1].append(extr_metrics[0])
        extr_nc[-1].append(extr_metrics[1])
        print(f'done with t{target_num_matching} p{prox}')
        print(extr_metrics)

print('extr_nc')
print('\n'.join(['\t'.join([f'{num}' for num in row]) for row in extr_nc]))
print()
print('extr_vol')
print('\n'.join(['\t'.join([f'{num}' for num in row]) for row in extr_vol]))
