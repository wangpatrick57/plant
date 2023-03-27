#!/bin/python3
from all_helpers import *
import sys
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='run_blant.py', description='A wrapper around BLANT (Algorithm 1 in the paper) that integrates into the plant data/ and networks/ ecosystem')
    parser.add_argument('gtag', help='The graph tag (gtag) of the graph to run BLANT on')
    args = parser.parse_args()
    p, _ = run_blant(args.gtag, algo=None)

    if p != None:
        p.wait()
