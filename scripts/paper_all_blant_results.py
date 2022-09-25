#!/pkg/python/3.7.4/bin/python3
from all_helpers import *
import sys

pairs = get_paper_all_pairs()
algo = 'stairs'

for gtag1, gtag2 in pairs:
    seeds, seed_metrics, extr_metrics = simplified_run_with_metrics(gtag1, gtag2, algo=algo, silent=True)
    to_print = [f'{gtag1}-{gtag2}', len(seeds), seed_metrics[0], seed_metrics[1], extr_metrics[0], extr_metrics[1]]
    print('\t'.join([str(e) for e in to_print]))
