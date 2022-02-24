#!/bin/bash
species=$1
top_thousandth=$2
orbit=$3
el_file="/home/sana/Jurisica/IID/networks/IID${species}.el"
orca4_file="${el_file}.orca4"
out_file="${HOME}/plant/data/seeding_cached_data/blant_out/p${top_thousandth}-o${orbit}-${species}-lDEG2.out"

cd ~/BLANT
~/BLANT/blant -k8 -lDEG2 -mi -sINDEX -o$orbit -T$top_thousandth -f$orca4_file $el_file > $out_file
cd -

dedup.sh $out_file
