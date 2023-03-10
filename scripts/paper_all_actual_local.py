#!/bin/python3
from all_helpers import *
from run_sag import run_sag

pairs = get_iid_mammal_pairs()
MAX_INDICES = 1
SIMS_THRESHOLD = -0.95

for gtag1, gtag2 in pairs:
    alignment, size, nc, s3 = run_sag(gtag1, gtag2, MAX_INDICES, SIMS_THRESHOLD)
    print(f'{gtag1}-{gtag2}', size, nc, s3, sep='\t')