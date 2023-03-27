#!/bin/bash
nif1=$1
nif2=$2
ort=$3
out=$4
time=$out.time

cd $MCL_DIR
{ time ./alignMCL.sh $nif1 $nif2 $ort $out 2>&1 ; } 2> $time
cd -
