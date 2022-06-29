#!/pkg/python/3.7.4/bin/python3
from all_helpers import *
import sys

pairs = get_paper_all_pairs()
start = int(sys.argv[1])

for gtag1, gtag2 in pairs[start:start + 18]:
    seeds, seed_metrics, extr_metrics = low_param_one_run(*get_gtag_run_info(gtag1, gtag2))
    to_print = [f'{gtag1}-{gtag2}', len(seeds), seed_metrics[0], seed_metrics[2], extr_metrics[0], extr_metrics[1]]
    print('\t'.join([str(e) for e in to_print]))
