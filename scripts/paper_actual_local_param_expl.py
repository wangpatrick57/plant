#!/bin/python3
import sys
from run_sag import run_sag

gtag1 = sys.argv[1]
gtag2 = sys.argv[2]

MAX_INDICES = 1
sims_threshold_list = [-0.8, -0.82, -0.84, -0.86, -0.88, -0.9, -0.92, -0.94, -0.96, -0.98]
results = []
sep = '\t'

for sims_threshold in sims_threshold_list:
    alignment, size, nc, s3 = run_sag(gtag1, gtag2, MAX_INDICES, sims_threshold, overwrite=True)
    results.append(f'{size}{sep}{nc:.3f}')

print('\n'.join(results))