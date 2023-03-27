#!/bin/python3
from all_helpers import *

# HOW TO USE SLURM
# run ./mcl_slurm_tool.py | distrib_slurm [jobname] --ntasks-per-node 1
# use squeue (after module load slurm) to see currently running jobs

# SLURM BEHAVIOR
# sometimes the log files contain partial output before the program is actually done. don't be surprised by this

mode = 'full'
notes = 'no1'

for gtag1, gtag2 in get_tprl_pairs():
    print(f'run_mcl.py {mode} {gtag1} {gtag2} {notes}')
