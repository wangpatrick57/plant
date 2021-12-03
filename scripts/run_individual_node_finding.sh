#!/bin/bash
SPECIES1=$1
SPECIES2=$2
PERCENT=$3
ORBIT=$4
ODV_DIR=/home/sana/Jurisica/IID/networks
SEEDS_FILE=${HOME}/plant/data/combine/seeds-p${PERCENT}-o${ORBIT}-${SPECIES1}-${SPECIES2}.out
NODES_FILE=${HOME}/plant/data/combine/nodes-p${PERCENT}-o${ORBIT}-${SPECIES1}-${SPECIES2}.out
RESULTS_FILE=${HOME}/plant/data/combine/results-p${PERCENT}-o${ORBIT}-${SPECIES1}-${SPECIES2}.out

extract_node_pairs_from_seeds.py $SEEDS_FILE >$NODES_FILE
evaluate_nodes.py $SPECIES1 $SPECIES2 $NODES_FILE 2>$RESULTS_FILE
