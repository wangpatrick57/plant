#!/bin/python3
from all_helpers import *
import sys
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='run_blant.py', description='A convenience wrapper around BLANT (Algorithm 1 in the paper)')
    parser.add_argument('gtag', help='The graph tag (gtag) of the graph to run BLANT on')
    parser.add_argument('-a', '--algo', default='stairs', help='Which BLANT variation to use. BLANT executables are compiled in the format blant{algo} based on their variation')
    args = parser.parse_args()
    p, _ = run_blant(args.gtag, algo=args.algo)

    if p != None:
        p.wait()
