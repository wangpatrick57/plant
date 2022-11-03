#!/pkg/python/3.7.4/bin/python3
from all_helpers import *
import sys

gtag = sys.argv[1]
k = int(sys.argv[2])
n = int(sys.argv[3])
p, _ = run_blant_sample(gtag, k, n, overwrite=False)

if p != None:
    p.wait()
