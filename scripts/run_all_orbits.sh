#!/bin/bash
species=$1
percent=$2

for orbit in {0..14}; do
    run_blant_t_o.sh $species $percent $orbit
done
