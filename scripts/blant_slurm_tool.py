#!/pkg/python/3.7.4/bin/python3
from all_helpers import *

# HOW TO USE SLURM
# run ./blant_slurm_tool.py | /home/sana/bin/distrib_slurm [jobName] --ntasks-per-node 1
# use squeue (after module load slurm) to see currently running jobs

# SLURM BEHAVIOR
# sometimes the log files contain partial output before the program is actually done. don't be surprised by this

jobname = 'nov16aft'

for gtag in get_paper_all_gtags():
    for algo in [6, 7]: # "algo" really means k
        print(f'./blant_wrapper.sh {jobname} {gtag} {algo}')

