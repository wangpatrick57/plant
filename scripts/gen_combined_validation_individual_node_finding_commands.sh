#!/bin/bash
for species1 in horse human mouse pig rabbit rat; do
    for species2 in horse human mouse pig rabbit rat; do
        for p in 0 1; do
            for o in 0 1; do
                echo "run_individual_node_finding.sh $species1 $species2 $p $o"
            done
        done
    done
done
