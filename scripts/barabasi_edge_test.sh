#!/bin/bash
ulimit -s unlimited

for num_edges in 60000 70000 80000 90000 100000 110000 120000 130000 140000 150000; do
    for trial_num in 1 2 3 4 5; do
        python3 hairball_graph_gen.py $num_edges >/dev/null
        cd ~/oldBLANT/BLANT
        num_graphlets=`./blant -k8 -lDEG1 -mi -sINDEX ~/plant/networks/hairball/barabasi_test.el 2>/dev/null | wc -l`
        echo "$num_edges $num_graphlets $trial_num"
        cd ~/plant/scripts
    done
done
