#!/bin/bash
species1=$1
species2=$2
pprox_max=$3
mode=$4

get_indexes_file() {
    echo "$HOME/plant/data/zhi/table/${1}_k8_l2_ninf_oldBlant.txt"
}

SCRIPTS_DIR="$HOME/plant/scripts"
tmp_file_name="$species1_$species2_tmp_seeds_file.txt"
tmp_file="/tmp/$tmp_file_name"
s1_indexes_file=`get_indexes_file $species1`
s2_indexes_file=`get_indexes_file $species2`

for (( pprox=1; pprox<=pprox_max; pprox++ )); do
    python3 $SCRIPTS_DIR/patching_algorithm.py 8 $species1 $species2 $s1_indexes_file $s2_indexes_file 6 $pprox >$tmp_file 2>/dev/null
    python3 $SCRIPTS_DIR/create_table_row.py 10 $species1 $species2 $tmp_file $mode
done
