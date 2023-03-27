## Contents
Below, the main directories and non-self-explanatory files are explained
* alignMCL - the source code for the AlignMCL algorithm
* core_algorithms - code that performs the core logic of the seed creation and merging algorithms
* helpers - various helpers for code which is often reused, such as managing network files, managing various forms of cached data, manipulating network or alignment objects, calculating statistics and other metrics, etc.
* main_runnable_programs - standardized command line interfaces for the main algorithms, as well as tools to easily run the algorithms using SLURM on Openlab
* paper_result_scripts - ready scripts which reproduce results in the paper
* tools - various exploratory, testing, and utility tools
  * graphsh.py - a tool to explore graphs through a shell-like interface
  * nauty_patch_correspondence - a tool to convert patch IDs to canonical IDs using NAUTY
  * pyblant.py - a Python reimplementation of BLANT for exploratory use
## Setup
clone BLANT and AlignMCL as well
describe gtags
