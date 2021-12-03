#!/bin/bash
for t in 0 1; do
    for o in 0 1 2 3 4 5 6 7 8 9 10 11 12 13; do
        for species in horse human mouse pig rabbit rat; do
            echo "run_blant_t_o.sh $t $o $species"
        done
    done
done
