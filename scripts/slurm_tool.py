#!/pkg/python/3.7.4/bin/python3
from all_helpers import *

# gtags = get_paper_all_gtags()
pairs = get_biogrid_induced_pairs() + get_biogrid_pairs()
jobname = 'j26night2'
notes = 'no1'

for gtag1, gtag2 in pairs:
    print(f'./mcl_wrapper.sh {jobname} {gtag1} {gtag2} {notes}')

