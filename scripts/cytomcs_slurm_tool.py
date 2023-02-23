#!/pkg/python/3.7.4/bin/python3
from all_helpers import *

# HOW TO USE SLURM
# run ./cytomcs_slurm_tool.py | /home/sana/bin/distrib_slurm [jobName] --ntasks-per-node 1
# use squeue (after module load slurm) to see currently running jobs

# SLURM BEHAVIOR
# sometimes the log files contain partial output before the program is actually done. don't be surprised by this

jobname = 'feb16aft2'
pairs = get_iid_mammal_pairs()
# pairs = [('human', 'pig'), ('mouse', 'rabbit'), ('rabbit', 'rat')]
perturbation = 0
max_num_steps = 0
random_seed = 0

for gtag1, gtag2 in pairs:
    print(f'./cytomcs_wrapper.sh {jobname} {gtag1} {gtag2} {perturbation} {max_num_steps} {random_seed}')

