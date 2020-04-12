# SISE 15-puzzle solver

SISE 15-puzzle solver is a project which was made for my university classes.
This solver uses BFS, DFS and A* algorithms (Manhattan and Hamming metrics included).
You can also set search order for BFS and DFS algorithms.

## Input data

This solver can operate on many different shapes of input puzzles. Default values are set for classic 4x4 puzzle.

Input file should look like this:

```bash
4 4
1 2 3 4
5 6 7 8
9 10 11 0
13 14 15 12
```

Where numbers in first line are puzzle's height and puzzle's width.

## Usage

```bash
pyhon main.py algorithm search_order/metric input_filename output_filename output_filename_2
```

* **search_order (permutation of 4 letters)**
    * ldur
    * drul
    * rdul
    * etc.
* **metric**
    * hamm - for Hamming distance
    * manh - for Manhattan distance
* **input_filename**  
    * name of input file
* **output_filename**
    * name of first output file
* **output_filename_2**
    * name of second output file

Output files include such things like: length of solution, execution time, number of visited and processed nodes.

plot_gen.py was only used to generate plots for educational purposes.