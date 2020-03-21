import sys
import time
import numpy as np

from puzzle import Puzzle
from bfs import Bfs
from dfs import Dfs

# default values for height and width
puzzle_width = puzzle_height = 4


def print_initial_info(args, loaded_puzzle):

    print("""
Initial arguments list:
Strategy: {}
Search order or heuristic: {}
Input filename: {}
Output filename: {}
Additional filename: {}
Loaded state of puzzle: \n\n{}\n""".format(*args, loaded_puzzle))


def load_initial_puzzle(filename):

    global puzzle_height, puzzle_width

    with open(filename, 'r') as f:
        puzzle_height, puzzle_width = [int(value) for value in f.readline().strip("\r\n").split(" ")]

    return np.loadtxt(filename, dtype=int, skiprows=1)


def generate_correct_state(height, width):

    correct = np.arange(1, height * width + 1).reshape(height, width)
    correct[height - 1][width - 1] = 0
    return correct


def use_bfs(initial_state, order):
    
    bfs = Bfs(initial_state, order)
    start_time = time.perf_counter()
    result = bfs.run_search()
    end_time = time.perf_counter()
    
    print("""Solution string: {}
Max depth: {}
Number of visited: {}
Number of processed: {}
Execution time: {} seconds""".format(*result, end_time - start_time))


def use_dfs(initial_state, order):

    dfs = Dfs(initial_state, order)
    start_time = time.perf_counter()
    result = dfs.run_search()
    end_time = time.perf_counter()
    
    print("""Solution string: {}
Max depth: {}
Number of visited: {}
Number of processed: {}
Execution time: {} seconds""".format(*result, end_time - start_time))


def use_a_star():
    pass


def choose_method(method, order, initial_state):

    switch_by_method = {
    'bfs': use_bfs,
    'dfs': use_dfs,
    'astr': use_a_star
    }
    method_to_use = switch_by_method.get(method.lower(), "Wrong method!")
    return method_to_use(initial_state, order.lower())


def main():

    args = sys.argv[1:]

    if len(args) != 5:
        raise ValueError("Parsed amount of args is equal {}, missing arguments!".format(len(args)))
    else:
        initial_puzzle = load_initial_puzzle(args[2])
        print_initial_info(args, initial_puzzle)
        correct_puzzle = generate_correct_state(puzzle_height, puzzle_width)
        
        Puzzle.correct_state, Puzzle.puzzle_height, Puzzle.puzzle_width = correct_puzzle, puzzle_height, puzzle_width

        first_state = Puzzle(initial_puzzle)
        choose_method(args[0], args[1], first_state)



if __name__ == "__main__":
    main()