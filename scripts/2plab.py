#!/pkg/python/3.7.4/bin/python3
from all_helpers import *
import sys

for gtag1, gtag2 in get_biogrid_induced_pairs():
    wayne_copy_mcl(gtag1, gtag2, notes='no1')
