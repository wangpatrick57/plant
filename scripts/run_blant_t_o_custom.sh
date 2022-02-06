#!/bin/bash
species=$1
top_thousandth=$2
orbit=$3
el_file=$4
out_file=$5
orca4_file="/home/sana/Jurisica/IID/networks/IID${species}.el.orca4"

cd ~/BLANT
~/BLANT/blant -k8 -lDEG2 -mi -sINDEX -o$orbit -T$top_thousandth -f$orca4_file $el_file > $out_file
cd -

dedup.sh $out_file
