#!/pkg/python/3.7.4/bin/python3
from all_helpers import *
import sys

if __name__ == '__main__':
    from seeding_algorithm_core import SeedingAlgorithmSettings
    
    gtag1 = sys.argv[1]
    gtag2 = sys.argv[2]
    seeds, seed_metrics, extr_metrics = simplified_run_with_metrics(gtag1, gtag2, settings=SeedingAlgorithmSettings(2, 0, 1))
    print(len(seeds), seed_metrics)
