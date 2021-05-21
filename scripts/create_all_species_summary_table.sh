#!/bin/bash
species_order="cat chicken cow dog duck fly horse human mouse pig rabbit rat sheep turkey worm"
echo $species_order
out_arr=()
cut_start=1

for species1 in $species_order; do
    for species2 in `echo $species_order | cut -d' ' -f $cut_start-`; do
        out_arr+=(`./create_full_table.sh $species1 $species2 1 SUMMARY`)
    done

    echo "${out_arr[@]}"
    out_arr=()
    cut_start=$(( $cut_start + 1 ))
done
