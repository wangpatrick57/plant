#!/pkg/python/3.7.4/bin/python3
from all_helpers import *

# HOW TO USE SLURM
# run ./odvorts_slurm_tool.py | /home/sana/bin/distrib_slurm [jobName] --ntasks-per-node 1
# use squeue (after module load slurm) to see currently running jobs

# SLURM BEHAVIOR
# sometimes the log files contain partial output before the program is actually done. don't be surprised by this

jobname = 'oct15mn2'
notes = 'no1'

for gtag1, gtag2 in get_syeast_pairs():
    for k in range(1, 6):
        print(f'./odvorts_wrapper.sh {jobname} {gtag1} {gtag2} {k} {notes}')

