#!/pkg/python/3.7.4/bin/python3
from all_helpers import *
import sys

if __name__ == '__main__':
    max_num_steps = 0
    perturbation = 0
    gtag1 = sys.argv[1]
    gtag2 = sys.argv[2]

    print(f'sweeping seeds for {gtag1}-{gtag2} s{max_num_steps} p{perturbation}')

    for random_seed in range(10):
        alignment_path = get_cytomcs_alignment_path(gtag1, gtag2, perturbation=perturbation, max_num_steps=max_num_steps, random_seed=random_seed)

        if os.path.exists(alignment_path):
            size, nc, s3 = run_cytomcs_for_pair(gtag1, gtag2, max_num_steps=max_num_steps, perturbation=perturbation, random_seed=random_seed, overwrite=False, silent=True)

            print(f'r{random_seed} | ', end='')

            if nc < 0.15:
                print('bad', end='')
            elif nc > 0.8:
                print('good', end='')
            else:
                print('weird', end='')

            print(f' (nc={nc})')
        else:
            print(f'skipping r{random_seed}')
