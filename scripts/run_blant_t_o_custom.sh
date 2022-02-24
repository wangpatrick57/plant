#!/bin/bash
top_thousandth=$1
orbit=$2
lDEG=$3
el_file=$4
orca4_file=$5
out_file=$6

cd ~/BLANT
~/BLANT/blant -k8 -lDEG$lDEG -mi -sINDEX -o$orbit -T$top_thousandth -f$orca4_file $el_file > $out_file
cd -

dedup.sh $out_file
