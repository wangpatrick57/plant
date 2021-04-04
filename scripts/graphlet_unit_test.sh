#!/bin/bash

while read p;
do
    python3 gen_graphlet_58.py $p > /home/wangph1/plant/networks/tempnet.el
    cd /home/wangph1/BLANT
    ./blant -k6 -sINDEX -mi /home/wangph1/plant/networks/tempnet.el > /home/wangph1/plant/data/k6max/tempdata.txt
    cd /home/wangph1/plant/scripts
    num_lines=$(wc -l /home/wangph1/plant/data/k6max/tempdata.txt | cut -c1-1)

    if (( $num_lines != "1" ))
    then
        echo "${p} had ${num_lines} lines"
    fi
done < permutations.txt
