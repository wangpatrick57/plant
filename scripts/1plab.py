#!/pkg/python/3.7.4/bin/python3
from all_helpers import *

for gtag in get_all_syeasts():
    for override_k in range(1, 6):
        run_orca_for_gtag(gtag, override_k=override_k)
