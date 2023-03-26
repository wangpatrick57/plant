#!/bin/bash
awk 'NR==FNR{arr[$0];next} $0 in arr' $1 $2
