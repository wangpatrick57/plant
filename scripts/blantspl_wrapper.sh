#!/bin/bash
jobname=$1
gtag=$2
k=$3
n=$4

# setup
scrname="blantsample"
LOG_DIR=~/plant/data/slurm_logs/$scrname/$jobname
mkdir -p $LOG_DIR
logf=$LOG_DIR/$scrname-$jobname-$gtag-$k-$n.log
startlogf=$LOG_DIR/$scrname-$jobname-starts.log
endlogf=$LOG_DIR/$scrname-$jobname-ends.log

# running
echo "run_blantspl_tool.py $gtag $k $n &>$logf"
echo $logf >>$startlogf
run_blantspl_tool.py $gtag $k $n &>$logf

# end
echo "JOBSFINISHED" >>$logf
echo $logf >>$endlogf
