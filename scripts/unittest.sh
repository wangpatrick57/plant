#!/bin/bash
seeding_algorithm_core.py &>/dev/null
if [ $? -ne 0 ]; then echo "seeding_algorithm_core.py failed"; exit 1; fi

file_helpers.py &>/dev/null
if [ $? -ne 0 ]; then echo "file_helpers.py failed"; exit 1; fi

echo "ALL SUCCEEDED"
