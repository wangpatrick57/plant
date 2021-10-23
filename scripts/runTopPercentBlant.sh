#!/bin/bash
species=$1
top_percent=$2
out_path=$HOME/plant/data/zhi/expansion_methods/${species}_k8_l2_top${top_percent}exp.txt

BLANT_DIR="$HOME/oldBLANT/BLANT"
cd $BLANT_DIR
ulimit -s unlimited
./blant -k8 -lDEG2 -mi -sINDEX -T$top_percent /home/sana/Jurisica/IID/networks/IID${species}.el >$out_path
$HOME/plant/scripts/dedup.sh $out_path
cd - &>/dev/null
