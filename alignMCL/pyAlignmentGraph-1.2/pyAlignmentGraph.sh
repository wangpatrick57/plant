#!/bin/bash

PPI1=$1
PPI2=$2
ORT=$3
AG_NAME=$4

export PYTHONPATH=${PYTHONPATH}:./src
python src/pyAlignmentGraph.py --ppi1 $PPI1 --ppi2 $PPI2 --ort $ORT --ag $AG_NAME

