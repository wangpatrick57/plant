#!/pkg/python/3.7.4/bin/python3
from all_helpers import *

# HOW TO USE SLURM
# run ./sag_slurm_tool.py | /home/sana/bin/distrib_slurm [jobName] --ntasks-per-node 3
# use squeue (after module load slurm) to see currently running jobs

# SLURM BEHAVIOR
# sometimes the log files contain partial output before the program is actually done. don't be surprised by this

jobname = 'mar2aft1'
# pairs = get_paper_all_pairs()
pairs = get_iid_representative_pairs()
# max_indices_list = [3, 4, 5]
# sims_threshold_list = [-0.78, -0.8, -0.82, -0.84, -0.86, -0.88, -0.9, -0.92, -0.94]
max_indices_list = [4]
sims_threshold_list = [-0.78]

for gtag1, gtag2 in pairs:
    for max_indices in max_indices_list:
        for sims_threshold in sims_threshold_list:
            print(f'./run_sag.py {gtag1} {gtag2} {max_indices} {sims_threshold}')

