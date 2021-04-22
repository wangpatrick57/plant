#!/bin/bash
echo "before: `wc -l $1`"
awk '!visited[$0]++' $1 > .temptemptemp.txt
rm $1
mv .temptemptemp.txt $1
echo "after: `wc -l $1`"
