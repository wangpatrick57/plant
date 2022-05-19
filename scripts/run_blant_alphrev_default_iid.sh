#!/bin/bash
iid_species=$1
el_file="/home/sana/Jurisica/IID/networks/IID${iid_species}.el"
alph_file="${HOME}/plant/data/seeding_cached_data/blant_out/p0-o0-${iid_species}-lDEG2-alph.out"
rev_file="${HOME}/plant/data/seeding_cached_data/blant_out/p0-o0-${iid_species}-lDEG2-rev.out"

run_blant_default_custom.sh $el_file 2 1 $alph_file
run_blant_default_custom.sh $el_file 2 0 $rev_file
