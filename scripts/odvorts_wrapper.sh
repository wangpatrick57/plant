#!/bin/bash
jobname=$1
gtag1=$2
gtag2=$3
k=$4
notes=$5

# setup
scrname="odvorts"
LOG_DIR=~/plant/data/slurm_logs/$scrname/$jobname
mkdir -p $LOG_DIR
logf=$LOG_DIR/$scrname-$jobname-$gtag1-$gtag2-$k-$notes.log
startlogf=$LOG_DIR/$scrname-$jobname-starts.log
endlogf=$LOG_DIR/$scrname-$jobname-ends.log

# running
echo "run_odvorts_tool.py $gtag1 $gtag2 $k $notes &>$logf"
echo $logf >>$startlogf
# run_odvorts_tool.py $gtag1 $gtag2 $k $notes &>$logf

# end
echo "JOBSFINISHED" >>$logf
echo $logf >>$endlogf
