#!/bin/bash

# THIS VARIABLE IS THE ONLY ONE THAT NEEDS TO BE CHANGED
# ======================================================
PLANT_REPO_DIR="/home/wangph1/plant"
# ======================================================

# set up PYTHONPATH
depth1_subdirectories=$(find "$PLANT_REPO_DIR" -maxdepth 1 -type d \( ! -name ".git" -a ! -name "__pycache__" \) | tail -n +2)
export PYTHONPATH=$(echo "$depth1_subdirectories" | tr '\n' ':' | sed 's/:$//')
