#!/bin/bash
seeding_algorithm_core.py &>/dev/null
if [ $? -ne 0 ]; then echo "seeding_algorithm_core.py failed"; exit 1; fi
echo "seeding_algorithm_core.py succeeded"

file_helpers.py &>/dev/null
if [ $? -ne 0 ]; then echo "file_helpers.py failed"; exit 1; fi
echo "file_helpers.py succeeded"

full_algorithm_helpers.py &>/dev/null
if [ $? -ne 0 ]; then echo "full_algorithm_helpers.py failed"; exit 1; fi
echo "full_algorithm_helpers.py succeeded"

echo "ALL SUCCEEDED"
