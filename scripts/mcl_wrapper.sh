#!/bin/bash
jobname=$1
gtag1=$2
gtag2=$3
notes=$4

# setup
scrname="mcl"
LOG_DIR=~/plant/data/slurm_logs/$scrname/$jobname
mkdir -p $LOG_DIR
logf=$LOG_DIR/$scrname-$jobname-$gtag1-$gtag2.log
startlogf=$LOG_DIR/$scrname-$jobname-starts.log
endlogf=$LOG_DIR/$scrname-$jobname-ends.log

# running
echo $logf >>$startlogf
mcl_helpers.py full $gtag1 $gtag2 $notes &>$logf

# end
echo "JOBSFINISHED" >>$logf
echo $logf >>$endlogf
