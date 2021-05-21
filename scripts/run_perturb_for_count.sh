#!/bin/bash
PERTURB_SCRIPT="$HOME/plant/scripts/perturb_el.py"
PATCHING_SCRIPT="$HOME/plant/scripts/patching_algorithm.py"
BLANT_DIR="$HOME/oldBLANT/BLANT"
s1_name="rat"
s2_name="mouse"
s1_og_file="/home/sana/Jurisica/IID/networks/IID${s1_name}.el"
s2_og_file="/home/sana/Jurisica/IID/networks/IID${s2_name}.el"

perturb_count=$1
trial=$2
s1_pr_file="$HOME/plant/networks/zhi/perturb/${s1_name}_${perturb_count}_${trial}.el"
s2_pr_file="$HOME/plant/networks/zhi/perturb/${s2_name}_${perturb_count}_${trial}.el"
s1_data_file="$HOME/plant/data/zhi/perturb/${s1_name}_${perturb_count}_${trial}.txt"
s2_data_file="$HOME/plant/data/zhi/perturb/${s2_name}_${perturb_count}_${trial}.txt"

python3 $PERTURB_SCRIPT $s1_og_file $perturb_count >$s1_pr_file
echo "$s1_name done perturbing for $perturb_count"
python3 $PERTURB_SCRIPT $s2_og_file $perturb_count >$s2_pr_file
echo "$s2_name done perturbing for $perturb_count"

cd $BLANT_DIR
ulimit -s unlimited
./blant -k8 -lDEG2 -mi -sINDEX $s1_pr_file >$s1_data_file
~/plant/scripts/dedup.sh $s1_data_file
echo "$s1_name done blanting for $perturb_count"
./blant -k8 -lDEG2 -mi -sINDEX $s2_pr_file >$s2_data_file
~/plant/scripts/dedup.sh $s2_data_file
echo "$s2_name done blanting for $perturb_count"
cd -
