#!/bin/bash
el_file=$1
lDEG=$2
out_file=$3
cd ~/BLANT
~/BLANT/blant -k8 -lDEG$lDEG -mi -sINDEX $el_file > $out_file
cd -

dedup.sh $out_file

