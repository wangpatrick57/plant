#!/bin/python3
import sys
from all_helpers import *

# THE RUN_SAG.PY FILE OVERWRITES, BUT THE PAPER_ALL_* FILES THAT CALL RUN_SAG DON'T OVERWRITE
if __name__ == '__main__':
    from seeding_algorithm_core import SeedingAlgorithmSettings
    
    gtag1 = sys.argv[1]
    gtag2 = sys.argv[2]
    max_indices = int(sys.argv[3])
    sims_threshold = float(sys.argv[4])
    
    seeds, _, _ = simplified_run_with_metrics(gtag1, gtag2, settings=SeedingAlgorithmSettings(max_indices=max_indices, sims_threshold=sims_threshold))
