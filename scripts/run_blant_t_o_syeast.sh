#!/bin/bash
yeast_name=$1
top_thousandth=$2
orbit=$3
lDEG=3
el_file="${HOME}/BLANT/networks/${yeast_name}/${yeast_name}.el"
orca4_file="${el_file}.orca4"
out_file="${HOME}/plant/data/seeding_cached_data/blant_out/p${top_thousandth}-o${orbit}-${yeast_name}-lDEG${lDEG}.out"

run_blant_t_o_custom.sh $top_thousandth $orbit $lDEG $el_file $orca4_file $out_file
