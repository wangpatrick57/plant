#!/bin/bash
cd ~/BLANT

k="6"
lDEG="2"
species="cat"

this_file="${HOME}/plant/data/topological_antidup/${species}shuf_k${k}l${lDEG}"
this_file_txt="${this_file}.txt"
this_file_sorted="${this_file}_sorted.txt"
other_file="${HOME}/plant/data/topological_antidup/${species}_k${k}l${lDEG}"
other_file_txt="${other_file}.txt"
other_file_sorted="${other_file}_sorted.txt"

base_network="/home/sana/Jurisica/IID/networks/IIDcat.el"
# base_network="${HOME}/BLANT/networks/syeast0/syeast0.el"
shuf_network="${HOME}/plant/networks/${species}_shuf.el"

./blant -k$k -lDEG$lDEG -sINDEX -mi -A $base_network >$other_file_txt
echo $base_network $other_file_txt
other_lines=$(cat $other_file_txt | wc -l)
echo "there are ${other_lines} lines total"
sort $other_file_txt >$other_file_sorted

for i in {1..5}
do
    shuf <$base_network >$shuf_network
    ./blant -k$k -lDEG$lDEG -sINDEX -mi -A $shuf_network >$this_file_txt
    sort $this_file_txt >$this_file_sorted
    diff_lines=$(diff $this_file_sorted $other_file_sorted | wc -l)
    lines=$(cat $this_file_txt | wc -l)

    if [ $other_lines != $lines ]
    then
        echo "DIFF NUM LINES"
        echo "${lines} in shuffled vs ${other_lines} in original"
    else
        echo "no diff in num of lines"
    fi

    if [ $diff_lines != "0" ]
    then
        echo "DIFF DETECTED"
        echo "${diff_lines} lines different out of ${lines}"
    else
        echo "no diff"
    fi

    unique_lines=$(cat $this_file_sorted | uniq -c | wc -l)

    if [ $unique_lines != $lines ]
    then
        echo "DUPLICATES DETECTED"
        echo "${unique_lines} unique lines out of ${lines} lines"
    else
        echo "no duplicates"
    fi
done

cd -
