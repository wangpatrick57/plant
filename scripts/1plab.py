#!/pkg/python/3.7.4/bin/python3
from all_helpers import *
import sys

for gtag in get_paper_all_gtags(base_tprl_only=True):
    print(gtag, gtag_to_real_name(gtag))
