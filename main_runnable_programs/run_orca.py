#!/bin/python3
from all_helpers import *
import sys
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='run_orca.py', description='Run ORCA, an algorithm which enumerates the orbit degree vector of every node in the graph')
    parser.add_argument('gtag', help='The graph tag (gtag) of the graph to run ORCA on')
    parser.add_argument('-k', '--override-k', type=int, default=-1, help='Override the way k is usually determined (by gtag_to_k())')
    args = parser.parse_args()

    if args.override_k == -1:
        override_k = None
    else:
        override_k = args.override_k
        assert override_k > 0

    run_orca_for_gtag(args.gtag, override_k=override_k)
