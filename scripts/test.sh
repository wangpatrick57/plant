s1=$1
s2=$2

# ./run_seeding_t_o.sh $s1 $s2 0 1
./run_combined_node_finding.sh $s1 $s2 0 1
less ~/plant/data/combine/combined-results-maxp0-o01-${s1}-${s2}.out
