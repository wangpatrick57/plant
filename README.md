## Contents
Below, the main directories and non-self-explanatory files are explained
* alignMCL - the source code for the AlignMCL algorithm
* core_algorithms - code that performs the core logic of the seed creation and merging algorithms
* helpers - various helpers for code which is often reused, such as managing network files, managing various forms of cached data, manipulating network or alignment objects, calculating statistics and other metrics, etc.
  * bash_helpers.py - helper functions to simplify the running of various external programs, most notably BLANT and AlignMCL
  * canonmaps_helpers.py - helper functions to process the files in the canon_maps/ directory
  * full_algorithm_helpers.py - helper functions that reduce the boilerplate code necessary to run programs
  * index_validation_helpers.py - helper functions to validate whether an index file is well-formed
  * orbit_mapping_helpers.py - helper functions to enable and speed up the processing ODVs of k > 5
  * top_node_analysis_helpers.py - helper functions for analyzing the nodes with the highest degree, which often generates useful insights
* main_runnable_programs - standardized command line interfaces for the main algorithms, as well as tools to easily run the algorithms using SLURM on Openlab
* paper_result_scripts - ready scripts which reproduce results in the paper
* tools - various exploratory, testing, and utility tools
  * graphsh.py - a tool to explore graphs through a shell-like interface
  * nauty_patch_correspondence - a tool to convert patch IDs to canonical IDs using NAUTY
  * pyblant.py - a Python reimplementation of BLANT for exploratory use
## Setup
clone BLANT and AlignMCL as well
describe gtags
