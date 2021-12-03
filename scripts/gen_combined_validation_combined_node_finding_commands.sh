#!/bin/bash
for species1 in horse human mouse pig rabbit rat; do
    for species2 in horse human mouse pig rabbit rat; do
        echo "run_combined_node_finding.sh $species1 $species2"
    done
done
