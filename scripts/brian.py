#!/bin/python3

from collections import defaultdict
import sys
import re
from odv_helpers import *
from statistics import mean

# # input
species1 = sys.argv[1]
species2 = sys.argv[2]

# ortho stuff
ortho_file = open('./Orthologs.Uniprot.tsv', 'r')
SPECIES_TO_INDEX = dict()
species_line = ortho_file.readline().strip()
species_order = re.split('[\s\t]+', species_line)
# species_order is an array of the types

ind1 = species_order.index(species1)
ind2 = species_order.index(species2)

for i in ortho_file:
    lineDict = i.strip().split()
    if lineDict[ind1] != 0 and lineDict[ind2] != 0:
        print(lineDict[ind1] + " " + lineDict[ind2])

