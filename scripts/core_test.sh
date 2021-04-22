#!/bin/bash
ulimit -s unlimited
out_file=$1

core_nodes=750
for core_edges in 1500; do
    ./single_core_test.sh $core_nodes $core_edges $out_file
done

core_nodes=1000
for core_edges in 2500; do
    ./single_core_test.sh $core_nodes $core_edges $out_file
done

core_nodes=1250
for core_edges in 3000 3500 4000; do
    ./single_core_test.sh $core_nodes $core_edges $out_file
done

core_nodes=1500
for core_edges in 4000 4500 5000; do
    ./single_core_test.sh $core_nodes $core_edges $out_file
done
