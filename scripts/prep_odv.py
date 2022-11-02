#!/bin/python3
from all_helpers import *

for gtag in get_paper_all_gtags():
    run_orca_for_gtag(gtag)
