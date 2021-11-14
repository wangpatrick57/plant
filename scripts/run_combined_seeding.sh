#!/bin/bash

# for percent from 0 to max:
    # for orbit in 0,2,5,7:
        # run nonpatch_seeding on mouse/rat output files, >> redirect to common output file

MAX_PERCENT=$1
SPECIES1=mouse
SPECIES2=rat
ODV_DIR=/home/sana/Jurisica/IID/networks

for percent in {0..$MAX_PERCENT} do
    for orbit in 0 2 5 7 do
        python3 nonpatch_seeding_algorithm.py 8 $SPECIES1 $SPECIES2                \
            ../data/combine/p${percent}-o${orbit}-${SPECIES1}-lDEG2.out            \
            ../data/combine/p${percent}-o${orbit}-${SPECIES2}-lDEG2.out            \
            ${ODV_DIR}/IID${SPECIES1}.el.orca4 ${ODV_DIR}/IID${SPECIES2}.el.orca4  \
            >> ../data/combine/combined-seeding-p${percent}.out
    done
done
