#!/bin/python3
from all_helpers import *

# HOW TO USE SLURM
# run sag_slurm_tool.py | distrib_slurm [jobName] --ntasks-per-node 1 --mem=10000
# use squeue (after module load slurm) to see currently running jobs

# SLURM BEHAVIOR
# sometimes the log files contain partial output before the program is actually done. don't be surprised by this

pairs = get_paper_all_pairs()

for gtag1, gtag2 in pairs:
    print(f'paper_sag_prog.py {gtag1} {gtag2}')

