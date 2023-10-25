# call-hierarchy-to-canvas

Convert a call graph from IntelliJ into an obsidian canvas file.

## Requirements

- Graphviz must be installed on the system. It is used as an intermediate step to calculate the layout of the graph.
- Python 3.8+
- Python Libraries: 
  - graphviz


## Usage

** Warning ** - Obsidian reserves the right to do whatever it wants with a canvas file loaded into memory. 
This includes reformatting, rearranging, and changing ids of elements. 
This script should be considered a ***first step*** in the process of documenting a call graph. 
Once you start working within obsidian with the canvas, there is no reverse engineering the canvas file back into a call graph.

Running the script will output the final canvas file to stdout.
It is recommended to pipe the output either to a file or to your clipboard via `pbcopy` (on Mac).

```bash

```bash
python execute.py -f sample-call-graph.txt
```

An example input file is included in the source directory (`sample-call-graph.txt`)
