#!/pkg/python/3.7.4/bin/python3
from all_helpers import *

# HOW TO USE SLURM
# edit this file to either use mcl_wrapper.sh or blant_wrapper.sh
# run ./slurm_tool.py | /home/sana/bin/distrib_slurm [jobName] --ntasks-per-node 1
# use squeue (after module load slurm) to see currently running jobs

# SLURM BEHAVIOR
# sometimes the log files contain partial output before the program is actually done. don't be surprised by this

jobname = 'oct13nn3'
algo = 'bno'

for gtag in get_tprl_gtags()[4:24]:
    print(f'./blant_wrapper.sh {jobname} {gtag} {algo}')

