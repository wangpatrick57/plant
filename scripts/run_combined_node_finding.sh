#!/bin/bash
SPECIES1=$1
SPECIES2=$2
MAX_PERCENT=1
COMBINED_SEEDS_FILE=${HOME}/plant/data/combine/combined-seeds-maxp${MAX_PERCENT}-o01-${SPECIES1}-${SPECIES2}.out
COMBINED_NODES_FILE=${HOME}/plant/data/combine/combined-nodes-maxp${MAX_PERCENT}-o01-${SPECIES1}-${SPECIES2}.out
COMBINED_RESULTS_FILE=${HOME}/plant/data/combine/combined-results-maxp${MAX_PERCENT}-o01-${SPECIES1}-${SPECIES2}.out

# clear out file
echo -n "" > $COMBINED_SEEDS_FILE

for percent in $( seq 0 $MAX_PERCENT ); do
    for orbit in 0 1; do
        SEEDS_FILE="${HOME}/plant/data/combine/seeds-p${percent}-o${orbit}-${SPECIES1}-${SPECIES2}.out"
        cat $SEEDS_FILE >> $COMBINED_SEEDS_FILE
    done
done

extract_node_pairs_from_seeds.py $COMBINED_SEEDS_FILE >$COMBINED_NODES_FILE
evaluate_nodes.py $SPECIES1 $SPECIES2 $COMBINED_NODES_FILE 2>$COMBINED_RESULTS_FILE
