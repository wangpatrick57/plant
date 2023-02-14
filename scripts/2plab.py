#!/pkg/python/3.7.4/bin/python3
from all_helpers import *
import sys

if __name__ == '__main__':
    max_num_steps = 1
    perturbation = 0
    gtag1 = sys.argv[1]
    gtag2 = sys.argv[2]
    random_seed = sys.argv[3]

    size, nc, s3 = run_cytomcs_for_pair(gtag1, gtag2, max_num_steps=max_num_steps, perturbation=perturbation, random_seed=random_seed, overwrite=True, silent=False)
