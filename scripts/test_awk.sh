#!/bin/bash
awk 'ARGIND==2 {
    print $0
}' input_file1 input_file2
