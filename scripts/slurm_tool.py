#!/pkg/python/3.7.4/bin/python3
from all_helpers import *

gtags = get_paper_all_gtags()
jobname = 'jl4nn'
algo = 'stairs'

for gtag in gtags:
    print(f'./blant_wrapper.sh {jobname} {gtag} {algo}')

