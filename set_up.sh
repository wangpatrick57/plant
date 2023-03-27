#!/bin/bash

# NOTE: do ". ./set_up.sh" instead of "./set_up.sh", since we're setting envvars

# ONLY THIS SECTION NEEDS TO BE MODIFIED
# ======================================================
export PLANT_REPO_DIR="$HOME/plant"
export BLANT_DIR="$HOME/BLANT"
export MCL_DIR="$HOME/alignMCL"
# if you're using your own data/ or networks/ directories instead of those in https://github.com/wangpatrick57/plant_supplementary, uncomment these
# if you're cloning plant_supplementary, it comes with a script to set these envvars automatically
# export PLANT_DATA_DIR="/path/to/your/data/dir"
# export PLANT_NETWORKS_DIR="/path/to/your/networks/dir"
# ======================================================

# set up PYTHONPATH
depth1_subdirectories=$(find "$PLANT_REPO_DIR" -maxdepth 1 -type d \( ! -name ".git" -a ! -name "__pycache__" \) | tail -n +2)
export PYTHONPATH=$(echo "$depth1_subdirectories" | tr '\n' ':' | sed 's/:$//')

# add main_runnable_programs to PATH
export PATH="$PATH:$PLANT_REPO_DIR/main_runnable_programs"
