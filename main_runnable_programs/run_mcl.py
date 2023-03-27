#!/bin/python3
import sys
from all_helpers import *
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='run_seeds.py', description='Run the seed finding algorithm (Algorithm 2 in the paper)')
    parser.add_argument('gtag1', help='The graph tag (gtag) of the first graph')
    parser.add_argument('gtag2', help='The graph tag (gtag) of the second graph')
    parser.add_argument('-o', '--ort-algo', default='no1', help='Which algorithm to use to generate the "AlignMCL orthologs')
    args = parser.parse_args()
    print(args)
    full_local_run_mcl(args.gtag1, args.gtag2, notes=args.ort_algo)