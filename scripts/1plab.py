#!/pkg/python/3.7.4/bin/python3
from all_helpers import *
import sys

if __name__ == '__main__':
    from seeding_algorithm_core import SeedingAlgorithmSettings
    
    gtag1 = sys.argv[1]
    gtag2 = sys.argv[2]
    max_indices = int(sys.argv[3])
    sims_threshold = float(sys.argv[4])
    seeds, seed_metrics, extr_metrics = simplified_run_with_metrics(gtag1, gtag2, settings=SeedingAlgorithmSettings(max_indices=max_indices, sims_threshold=sims_threshold))
    print(len(seeds), seed_metrics)
