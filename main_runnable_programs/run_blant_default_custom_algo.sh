#!/bin/bash
algo=$1
el_file=$2
lDEG=$3
alph=$4
out_file=$5

time_file="${out_file}.time"

if [[ -z "${BLANT_DIR}" ]]; then
  echo "BLANT_DIR is not set"
  exit 1
fi


cd $BLANT_DIR
{ time $BLANT_DIR/blant$algo -k8 -lDEG$lDEG -mi -sINDEX -a$alph $el_file 2>&1 >$out_file ; } 2> $time_file
cd -

tools/dedup.sh $out_file

