#!/bin/python3
import sys
from run_sag import run_sag

gtag1 = sys.argv[1]
gtag2 = sys.argv[2]

max_indices_list = [3, 4, 5]
sims_threshold_list = [-0.88, -0.9, -0.92, -0.94, -0.96, -0.98]
result_str_dir = dict()
sep = '\t'

for max_indices in max_indices_list:
    result_str_dir[max_indices] = dict()
    
    for sims_threshold in sims_threshold_list:
        alignment, size, nc, s3 = run_sag(gtag1, gtag2, max_indices, sims_threshold)
        result_str_dir[max_indices][sims_threshold] = f'{size}{sep}{nc:.3f}'

for sims_threshold in sims_threshold_list:
    for max_indices in max_indices_list:
        s = result_str_dir[max_indices][sims_threshold]
        print(s, end=sep)

    print()
