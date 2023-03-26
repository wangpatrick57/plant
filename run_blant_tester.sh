#!/bin/bash
el_file=$HOME/BLANT/networks/syeast0/syeast0.el
# el_file=$HOME/plant/networks/tester.el
out_file=$HOME/plant/data/seeding_cached_data/blant_out/tester.out

cd ~/BLANT
./blant -k8 -lDEG1 -M0 -mi -sINDEX $el_file >$out_file
cd -

dedup.sh $out_file
