#!/bin/bash
el_file=$1
lDEG=$2
alph=$3
out_file=$4
time_file="${out_file}.time"

cd ~/BLANT
{ time ~/BLANT/blant -k8 -lDEG$lDEG -mi -sINDEX -a$alph $el_file 2>&1 >$out_file ; } 2> $time_file
cd -

dedup.sh $out_file

