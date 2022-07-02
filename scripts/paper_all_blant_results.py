#!/pkg/python/3.7.4/bin/python3
from all_helpers import *
import sys

start = int(sys.argv[1])
pairs = get_low_volume_pairs()[start:start + 11]

for gtag1, gtag2 in pairs:
    seeds, seed_metrics, extr_metrics = low_param_one_run(*get_gtag_run_info(gtag1, gtag2, algo='stairs'))
    to_print = [f'{gtag1}-{gtag2}', len(seeds), seed_metrics[0], seed_metrics[2], extr_metrics[0], extr_metrics[1]]
    print('\t'.join([str(e) for e in to_print]))
