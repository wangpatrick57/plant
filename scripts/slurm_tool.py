#!/pkg/python/3.7.4/bin/python3
from all_helpers import *

pairs = get_low_volume_pairs()
gtags = gtags_from_pairs(pairs)
jobname = 'jl1morn'

for gtag in gtags:
    print(f'./blant_wrapper.sh {jobname} {gtag}')

