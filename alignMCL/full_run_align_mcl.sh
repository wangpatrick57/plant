#!/bin/bash
N=5000

echo "running with N=${N}"

OUTPUT_DIR=~/alignMCL/output

gtag1=$1
gtag2=$2

if [[ $gtag1 == *"syeast"* ]]
then
	k=5
else
	k=4
fi

nif1=${gtag1}_marked.nif
nif2=${gtag2}_marked.nif
ort=${gtag1}-${gtag2}-k${k}-n${N}.ort
out=${gtag1}-${gtag2}-k${k}-n${N}
time=$out.time
outtake $nif1 $OUTPUT_DIR
outtake $nif2 $OUTPUT_DIR
outtake $ort $OUTPUT_DIR
{ time ./alignMCL.sh $OUTPUT_DIR/$nif1 $OUTPUT_DIR/$nif2 $OUTPUT_DIR/$ort $OUTPUT_DIR/$out 2>&1 ; } 2> $OUTPUT_DIR/$time
outsend $OUTPUT_DIR/${out}.txt
