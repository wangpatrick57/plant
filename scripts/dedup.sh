#!/bin/bash
awk '!visited[$0]++' $1 > .temptemptemp.txt
rm $1
mv .temptemptemp.txt $1
