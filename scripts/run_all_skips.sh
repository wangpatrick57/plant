#!/bin/bash
species=$1
orbit=$2

for skip in {0..10}; do
    run_blant_t_o.sh $species $skip $orbit
done
