#!/pkg/python/3.7.4/bin/python3
from all_helpers import *
from paper_low_k import *
import sys

gtag = sys.argv[1]
algo = sys.argv[2]
# k = int(sys.argv[2])
p, _ = run_blant(gtag, algo=algo)

if p != None:
    p.wait()
