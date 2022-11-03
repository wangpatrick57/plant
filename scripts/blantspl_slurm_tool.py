#!/pkg/python/3.7.4/bin/python3
from all_helpers import *

# HOW TO USE SLURM
# run ./blantspl_slurm_tool.py | /home/sana/bin/distrib_slurm [jobName] --ntasks-per-node 1
# use squeue (after module load slurm) to see currently running jobs

# SLURM BEHAVIOR
# sometimes the log files contain partial output before the program is actually done. don't be surprised by this

jobname = 'nov2nt3'
n = 2_000_000
gtags = get_all_syeasts()
gtags += ['mouse', 'rat', 'cat', 'horse', 'human']

for gtag in gtags:
    for k in range(4, 9):
        print(f'./blantspl_wrapper.sh {jobname} {gtag} {k} {n}')

