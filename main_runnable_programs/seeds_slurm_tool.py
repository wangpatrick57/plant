#!/bin/python3
from all_helpers import *

# HOW TO USE SLURM
# run ./seeds_slurm_tool.py | distrib_slurm [jobName] --ntasks-per-node 1 --mem=10000
# use squeue (after module load slurm) to see currently running jobs

# SLURM BEHAVIOR
# sometimes the log files contain partial output before the program is actually done. don't be surprised by this

# pairs = get_iid_mammal_pairs()
pairs = get_tprl_pairs()
# pairs = get_iid_representative_pairs()
# pairs = get_tprl_representative_pairs()
MAX_INDICES = 1
# sims_threshold_list = [-0.8, -0.82, -0.84, -0.86, -0.88, -0.9, -0.92, -0.94, -0.96, -0.98]
sims_threshold_list = [-0.95]

for gtag1, gtag2 in pairs:
    for sims_threshold in sims_threshold_list:
        print(f'./run_seeds.py {gtag1} {gtag2} {MAX_INDICES} {sims_threshold}')
