#!/pkg/python/3.7.4/bin/python3
from all_helpers import *
import sys

if __name__ == '__main__':
    max_num_steps = 1
    perturbation = 0
    gtag1 = sys.argv[1]
    gtag2 = sys.argv[2]
    num_good = 0
    num_bad = 0
    weirds = []

    for random_seed in range(100):
        size, nc, s3 = run_cytomcs_for_pair(gtag1, gtag2, max_num_steps=max_num_steps, perturbation=perturbation, random_seed=random_seed, overwrite=True, silent=True)

        if nc < 0.1:
            num_bad += 1
        elif nc > 0.8:
            num_good += 1
        else:
            weirds.append((random_seed, nc))

        print(f'results after r{random_seed} | {gtag1}-{gtag2} s{max_num_steps} p{perturbation}: {num_good} good, {num_bad} bad, {weirds} weird')
