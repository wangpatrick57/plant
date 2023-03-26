#!/pkg/python/3.7.4/bin/python3
from all_helpers import *

# HOW TO USE SLURM
# run ./blantspl_slurm_tool.py | /home/sana/bin/distrib_slurm [jobName] --ntasks-per-node 1
# use squeue (after module load slurm) to see currently running jobs

# SLURM BEHAVIOR
# sometimes the log files contain partial output before the program is actually done. don't be surprised by this

jobname = 'nov3aft1'

for gtag in get_all_syeasts():
    for k in range(4, 7):
        print(f'./blantspl_wrapper.sh {jobname} {gtag} {k} {100_000_000}')
        print(f'./blantspl_wrapper.sh {jobname} {gtag} {k} {1_000_000_000}')
        print(f'./blantspl_wrapper.sh {jobname} {gtag} {k} {2_000_000_000}')
