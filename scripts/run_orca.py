#!/pkg/python/3.7.4/bin/python3
from all_helpers import *
import sys

gtag = sys.argv[1]
override_k = int(sys.argv[2]) if len(sys.argv) > 2 else None
run_orca_for_gtag(gtag, override_k=override_k)
