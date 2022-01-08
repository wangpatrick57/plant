#!/bin/bash
SPECIES1=$1
SPECIES2=$2
PERCENT=$3
ORBIT=$4
ODV_DIR=/home/sana/Jurisica/IID/networks
SEEDS_FILE=${HOME}/plant/data/combine/seeds-p${PERCENT}-o${ORBIT}-${SPECIES1}-${SPECIES2}.out

nonpatch_seeding_algorithm.py 8 $SPECIES1 $SPECIES2 ${HOME}/plant/data/combine/p${PERCENT}-o${ORBIT}-${SPECIES1}-lDEG2.out ${HOME}/plant/data/combine/p${PERCENT}-o${ORBIT}-${SPECIES2}-lDEG2.out ALL >$SEEDS_FILE

