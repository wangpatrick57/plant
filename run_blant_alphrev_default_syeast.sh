#!/bin/bash
yeast_name=$1
el_file="${HOME}/BLANT/networks/${yeast_name}/${yeast_name}.el"
alph_file="${HOME}/plant/data/seeding_cached_data/blant_out/p0-o0-${yeast_name}-lDEG2-alph.out"
rev_file="${HOME}/plant/data/seeding_cached_data/blant_out/p0-o0-${yeast_name}-lDEG2-rev.out"

run_blant_default_custom.sh $el_file 2 1 $alph_file
run_blant_default_custom.sh $el_file 2 0 $rev_file
