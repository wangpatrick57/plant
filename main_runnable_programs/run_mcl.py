#!/bin/python3
import sys
from all_helpers import *
import argparse

if __name__ == '__main__':
    gtag1 = sys.argv[1]
    gtag2 = sys.argv[2]
    notes = sys.argv[3]
    full_local_run_mcl(gtag1, gtag2, notes=notes)