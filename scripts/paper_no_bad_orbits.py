#!/bin/python3
from seeding_algorithm_core import *
from blant_cache_helpers import *

# input parameters (none, since there's only one test right now)

# test constants
k = 8
species1 = "mouse"
species2 = "rat"
lDEG = 2
percent = 0
max_length = 15
sim_threshold = 0.79

# output stored here

# run for all orbits
for orbit in range(0, 15):
    # run seeding
    s1_index_path = get_index_path(species1, percent=percent, orbit=orbit, lDEG=lDEG)
    s2_index_path = get_index_path(species2, percent=percent, orbit=orbit, lDEG=lDEG)

    # extract nodes

    # calculate orthonodes

# print output
