#!/bin/bash
jobname=$1
gtag1=$2
gtag2=$3
perturbation=$4
max_num_steps=$5
random_seed=$6

# setup
scrname="cytomcs"
LOG_DIR=~/plant/data/slurm_logs/$scrname/$jobname
mkdir -p $LOG_DIR
logf=$LOG_DIR/$scrname-$jobname-$gtag1-$gtag2-p$perturbation-s$max_num_steps-r$random_seed.log
startlogf=$LOG_DIR/$scrname-$jobname-starts.log
endlogf=$LOG_DIR/$scrname-$jobname-ends.log

# running
echo $logf >>$startlogf
./cytomcs_helpers.py $gtag1 $gtag2 $perturbation $max_num_steps $random_seed &>$logf

# end
echo "JOBSFINISHED" >>$logf
echo $logf >>$endlogf
