#!/bin/bash
algo=$1
el_file=$2
lDEG=$3
alph=$4
out_file=$5
k=$6

time_file="${out_file}.time"

cd ~/BLANT
{ time ~/BLANT/blant$algo -k$k -lDEG$lDEG -mi -sINDEX -a$alph $el_file 2>&1 >$out_file ; } 2> $time_file
cd -

dedup.sh $out_file

