#!/bin/bash
awk '{deg[$1]++; deg[$2]++} END{asort(deg, deg_sorted, "@val_num_desc"); asorti(deg, node_names, "@val_num_desc"); for (i = 1; i <= 100; ++i) {print node_names[i], deg_sorted[i]}}' $1
