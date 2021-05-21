#!/bin/bash
species1=$1
species2=$2

get_indexes_file() {
    echo "$HOME/plant/data/zhi/perturb/${1}_${2}_${3}.txt"
}

SCRIPTS_DIR="$HOME/plant/scripts"
tmp_file_name="$species1_$species2_tmp_seeds_file.txt"
tmp_file="/tmp/$tmp_file_name"

for edges in 500 1000 2000 4000 8000 16000; do
    echo "=== STARTING $edges EDGES ==="

    for trial in 1 2 3 4 5; do
        s1_indexes_file=`get_indexes_file $species1 $edges $trial`
        s2_indexes_file=`get_indexes_file $species2 $edges $trial`

        s1_lines=`cat $s1_indexes_file | wc -l`
        s2_lines=`cat $s2_indexes_file | wc -l`

        if [ -e $s1_indexes_file ] && [ $s1_lines -gt 0 ] && [ $s2_lines -gt 0 ]; then
            python3 $SCRIPTS_DIR/patching_algorithm.py 8 $species1 $species2 $s1_indexes_file $s2_indexes_file >$tmp_file
            python3 $SCRIPTS_DIR/create_table_row.py 10 $species1 $species2 $tmp_file
        fi
    done
done
