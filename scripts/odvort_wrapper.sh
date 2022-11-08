#!/bin/bash
jobname=$1
gtag1=$2
gtag2=$3
k=$4
bnstr=$5
notes=$6

# setup
scrname="odvort"
LOG_DIR=~/plant/data/slurm_logs/$scrname/$jobname
mkdir -p $LOG_DIR
logf=$LOG_DIR/$scrname-$jobname-$gtag1-$gtag2-$k-$notes.log
startlogf=$LOG_DIR/$scrname-$jobname-starts.log
endlogf=$LOG_DIR/$scrname-$jobname-ends.log

# running
echo "run_odvort_tool.py $gtag1 $gtag2 $k $bnstr $notes &>$logf"
echo $logf >>$startlogf
run_odvort_tool.py $gtag1 $gtag2 $k $bnstr $notes &>$logf

# end
echo "JOBSFINISHED" >>$logf
echo $logf >>$endlogf
