#!/pkg/python/3.7.4/bin/python3
from all_helpers import *

pairs = get_paper_all_pairs()
jobname = 'jl3mn3'
notes = 'no1'

for gtag1, gtag2 in pairs:
    print(f'./odv_ort_wrapper.sh {jobname} {gtag1} {gtag2} {notes}')

