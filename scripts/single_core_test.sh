#!/bin/bash
core_nodes=$1
core_edges=$2
out_file=$3

lDEG=2
graph_gen="$HOME/plant/scripts/hairball_graph_gen.py"
barabasi_Onl="$HOME/plant/networks/hairball/barabasi_Onl.el"
barabasi_Onl_wcore="$HOME/plant/networks/hairball/barabasi_Onl_wcore.el"
barabasi_Onr="$HOME/plant/networks/hairball/barabasi_Onr.el"
barabasi_Onr_wcore="$HOME/plant/networks/hairball/barabasi_Onr_wcore.el"
baraOnl_output="$HOME/plant/data/hairball/baraOnl_k8_l${lDEG}_ninf.txt"
baraOnr_output="$HOME/plant/data/hairball/baraOnr_k8_l${lDEG}_ninf.txt"
bara_patched_output="$HOME/plant/data/hairball/baraOn_patched.txt"
echo $baraOnl_output

python3 $graph_gen $core_nodes $core_edges
echo "follicle count base"
grep -o 'follicle' $barabasi_Onl | wc -l
echo
echo "core count base"
grep -o 'core'  $barabasi_Onl | wc -l
echo "follicle count wcore"
grep -o 'follicle' $barabasi_Onl_wcore | wc -l
echo
echo "core count wcore"
grep -o 'core'  $barabasi_Onl_wcore | wc -l

cd ~/oldBLANT/BLANT
echo $barabasi_Onr_wcore
./blant -k8 -lDEG$lDEG -mi -sINDEX $barabasi_Onl_wcore >$baraOnl_output
./blant -k8 -lDEG$lDEG -mi -sINDEX $barabasi_Onr_wcore >$baraOnr_output

cd -
echo >>$out_file
echo "$core_nodes $core_edges" >>$out_file
~/plant/scripts/dedup.sh $baraOnl_output
~/plant/scripts/dedup.sh $baraOnr_output
python3 ~/plant/scripts/patching_algorithm.py 8 mouse rat $baraOnl_output $baraOnr_output 6 1 Hairball >$bara_patched_output

echo "follicle count" >>$out_file
grep -o 'follicle'  | wc -l >>$out_file
echo "core count" >>$out_file
grep -o 'core' $bara_patched_output | wc -l >>$out_file
