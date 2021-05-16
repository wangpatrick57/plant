#!/bin/bash
get_graph_file() {
    echo "/home/sana/Jurisica/IID/networks/IID${1}.el"
}

get_indexes_file() {
    echo "$HOME/plant/data/zhi/table/${1}_k8_l2_ninf_oldBlant.txt"
}

BLANT_DIR="$HOME/oldBLANT/BLANT"
USAGE_MSG="Usage: run_blant_for_species.sh species"

if [ $# -ne 1 ]; then
    echo >&2 $USAGE_MSG
    echo >&2
    exit 1
fi

species=$1
graph_file=`get_graph_file $species`
indexes_file=`get_indexes_file $species`

echo $graph_file
echo $indexes_file

cd $BLANT_DIR &>/dev/null
ulimit -s unlimited
./blant -k8 -lDEG2 -mi -sINDEX $graph_file >$indexes_file
cd - &>/dev/null

~/plant/scripts/dedup.sh $indexes_file
