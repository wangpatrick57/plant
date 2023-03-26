#!/bin/python3
import sys
from all_helpers import *
import argparse

if __name__ == '__main__':
    from seeding_algorithm_core import SeedingAlgorithmSettings

    parser = argparse.ArgumentParser(prog='run_seeds.py', description='Run the seed finding algorithm (Algorithm 2 in the paper)')
    parser.add_argument('gtag1')
    parser.add_argument('gtag2')
    parser.add_argument('-m', '--max-indices', default=1, help='The maximum number of times the graphlet may appear in either index for it to be eligible to be used in a seed')
    parser.add_argument('-s', '--sims-threshold', default=-0.95, help='The minimum (if s>0) or maximum (if s<0) mean ODV similarity value of the seed for it to be included in the output')
    args = parser.parse_args()
    print(args)
    seeds, _, _ = simplified_run_with_metrics(args.gtag1, args.gtag2, settings=SeedingAlgorithmSettings(max_indices=args.max_indices, sims_threshold=args.sims_threshold))
