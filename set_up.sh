#!/bin/bash

# THESE VARIABLES ARE THE ONLY ONE THAT NEED TO BE CHANGED
# ======================================================
PLANT_REPO_DIR="$HOME/plant"
# ======================================================

# set up PYTHONPATH
depth1_subdirectories=$(find "$PLANT_REPO_DIR" -maxdepth 1 -type d \( ! -name ".git" -a ! -name "__pycache__" \) | tail -n +2)
export PYTHONPATH=$(echo "$depth1_subdirectories" | tr '\n' ':' | sed 's/:$//')

# add main_runnable_programs to PATH
export PATH="$PATH:$PLANT_REPO_DIR/main_runnable_programs"
