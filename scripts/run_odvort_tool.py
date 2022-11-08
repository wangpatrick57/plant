#!/bin/python3
from mcl_helpers import gen_odv_ort_file
import sys

gtag1 = sys.argv[1]
gtag2 = sys.argv[2]
k = int(sys.argv[3])
bnstr = sys.argv[4]
notes = sys.argv[5]

if bnstr == 'None':
    bnstr = None

gen_odv_ort_file(gtag1, gtag2, override_k=k, bnstr=bnstr, notes=notes)
