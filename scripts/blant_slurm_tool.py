#!/pkg/python/3.7.4/bin/python3
from all_helpers import *

# HOW TO USE SLURM
# run ./blant_slurm_tool.py | distrib_slurm [jobName] --ntasks-per-node 1 --mem=10000
# use squeue (after module load slurm) to see currently running jobs

# SLURM BEHAVIOR
# sometimes the log files contain partial output before the program is actually done. don't be surprised by this

jobname = 'mar24aft1'
algo = 'stairs'

for gtag in get_paper_all_gtags():
    print(f'./blant_wrapper.sh {jobname} {gtag} {algo}')

