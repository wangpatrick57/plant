#!/bin/bash
jobname=$1
gtag=$2

# setup
scrname="blantindex"
LOG_DIR=~/plant/data/slurm_logs/$scrname/$jobname
mkdir -p $LOG_DIR
logf=$LOG_DIR/$scrname-$jobname-$gtag.log
startlogf=$LOG_DIR/$scrname-$jobname-starts.log
endlogf=$LOG_DIR/$scrname-$jobname-ends.log

# running
echo $logf >>$startlogf
run_blant_tool.py $gtag &>$logf

# end
echo "JOBSFINISHED" >>$logf
echo $logf >>$endlogf
