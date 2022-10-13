#!/pkg/python/3.7.4/bin/python3
from all_helpers import *

# HOW TO USE SLURM
# edit this file to either use mcl_wrapper.sh or blant_wrapper.sh
# run ./slurm_tool.py | /home/sana/bin/distrib_slurm [jobName] --ntasks-per-node 1
# use squeue (after module load slurm) to see currently running jobs

jobname = 'oct11test'
notes = 'no1'

for gtag1, gtag2 in get_tprl_pairs():
    print(f'./mcl_wrapper.sh {jobname} {gtag1} {gtag2} {notes}')

