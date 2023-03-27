## Contents
Below, the directories and some of the less intuitive files are described
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
1. Clone and set up [BLANT](https://github.com/waynebhayes/BLANT) according to its README.md
2. Edit ```set_up.sh``` to point to the base location of this repo and the BLANT repo, and then run ```. ./set_up.sh``` to set the environment variables correctly
3. If reproducing the results in the paper, clone [plant_supplementary](https://github.com/wangpatrick57/plant_supplementary/blob/main/README.md) to download the necessary networks and cached data files. Follow its README.md accordingly
4. If you are not performing step 3, instead create the directories data/ and networks/ and set the environment variables ```PLANT_DATA_DIR``` and ```PLANT_NETWORKS_DIR``` to point to them
  * This step is necessary because the graph tag system (see ```graph_helpers.py```) allows convenient access of networks/ and data/ files for a given graph
  * Additionally, results for long-running (ranging from minutes to hours) algorithm runs are automatically cached in various subdirectories within data/
5. To ensure that all of this is working, run ```tools/e2e_test.py```
  * Don't worry about error messages. The test only fails if the program crashes. If the test succeeds, you should see the message
```=======================
END2END TESTS SUCCEEDED
=======================```
