#!/bin/bash
species=$1
top_thousandth=$2
orbit=$3
lDEG=2
el_file="/home/sana/Jurisica/IID/networks/IID${species}.el"
orca4_file="${el_file}.orca4"
out_file="${HOME}/plant/data/seeding_cached_data/blant_out/p${top_thousandth}-o${orbit}-${species}-lDEG2.out"

run_blant_t_o_custom.sh $top_thousandth $orbit $lDEG $el_file $orca4_file $out_file
