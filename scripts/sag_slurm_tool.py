#!/pkg/python/3.7.4/bin/python3
from all_helpers import *

# HOW TO USE SLURM
# run ./sag_slurm_tool.py | /home/sana/bin/distrib_slurm [jobName] --ntasks-per-node 3
# use squeue (after module load slurm) to see currently running jobs

# SLURM BEHAVIOR
# sometimes the log files contain partial output before the program is actually done. don't be surprised by this

jobname = 'mar10mn6'
pairs = get_iid_mammal_pairs()
# pairs = get_iid_representative_pairs()
MAX_INDICES = 1
SIMS_THRESHOLD = -0.95

for gtag1, gtag2 in pairs:
    print(f'./run_sag.py {gtag1} {gtag2} {MAX_INDICES} {SIMS_THRESHOLD}')

