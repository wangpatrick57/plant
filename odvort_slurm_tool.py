#!/pkg/python/3.7.4/bin/python3
from all_helpers import *

# HOW TO USE SLURM
# run ./odvort_slurm_tool.py | /home/sana/bin/distrib_slurm [jobName] --ntasks-per-node 1
# use squeue (after module load slurm) to see currently running jobs

# SLURM BEHAVIOR
# sometimes the log files contain partial output before the program is actually done. don't be surprised by this

jobname = 'nov4nt'
bnstr = 'None'

for gtag1, gtag2 in get_paper_all_pairs():
    for notes in ['no1']:
        k = two_gtags_to_k(gtag1, gtag2)
        print(f'./odvort_wrapper.sh {jobname} {gtag1} {gtag2} {k} {bnstr} {notes}')

