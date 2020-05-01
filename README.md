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
* **algorithm**
    * bfs - for BFS
    * dfs - for DFS
    * astr - for A*
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

plot_gen.py was only used for educational purposes and making plots for my classes. Content of this file should not be considered as example of good coding practices.

## Output example

Usage and example of output is shown below.

```bash
python main.py bfs rdlu 4x4_07_00191.txt first second

Initial arguments list:
Strategy: bfs
Search order or heuristic: rdlu
Input filename: 4x4_07_00191.txt
Output filename: first
Additional filename: second
Loaded state of puzzle:

[[ 1  0  3  4]
 [ 5  2  6  8]
 [ 9 11  7 12]
 [13 10 14 15]]

Solution string: drdldrr
Max depth: 7
Number of visited: 810
Number of processed: 378
Execution time: 31.136 ms
```

As you can see, we have all output information in console. There is no need to use output files.