#!/bin/bash

PPI1=$1
PPI2=$2
ORT=$3
OUT_FILE=$4

#export PYTHONPATH=${PYTHONPATH}:pyAlignmentGraph-1.2/src
/pkg/python/2.7.14/bin/python pyAlignmentGraph-1.2/src/pyAlignmentGraph.py --ppi1 $PPI1 --ppi2 $PPI2 --ort $ORT --ag ${OUT_FILE}.ag

if [ -s "${OUT_FILE}.ag" ]; then
    echo ".ag file not empty"
    ./mcl/bin/mcl ${OUT_FILE}.ag -o ${OUT_FILE}.txt -I 2.8 --abc
else
    echo ".ag file empty"
    touch ${OUT_FILE}.txt
fi

