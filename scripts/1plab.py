#!/pkg/python/3.7.4/bin/python3
from all_helpers import *
import sys

# first, test paper_low_k.py with "./paper_low_k.py mouse rat 6"
# then, run "./1plab.py | /home/sana/bin/distrib_slurm nov16aft2 --ntasks-per-node 1"

pairs = get_paper_all_pairs()

for gtag1, gtag2 in pairs:
    for k in [6, 7]:
        print(f'./paper_low_k.py {gtag1} {gtag2} {k}')
