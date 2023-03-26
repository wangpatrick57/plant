#!/bin/bash
el_file=$1
k=$2
n=$3
out_file=$4

cd ~/BLANT
~/BLANT/blant -k$k -n$n -mo -sMCMC $el_file 2>&1 >$out_file
cd -

