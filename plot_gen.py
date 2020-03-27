import sys
import time
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from puzzle import Puzzle
from bfs import Bfs
from dfs import Dfs
from astr import Astr


labels = [1,2,3,4,5]
direction_orders = ["rdul", "rdlu", "drul", "drlu", "ludr", "lurd", "uldr", "ulrd"]
heuristics = ["manh", "hamm"]


def load_initial_puzzle(filename):
    return np.loadtxt("to_draw/" + filename, dtype=int, skiprows=1)  


def generate_correct_state(height = 4, width = 4):

    correct = np.arange(1, height * width + 1).reshape(height, width)
    correct[height - 1][width - 1] = 0
    return correct



def draw_by_solution_length(result):


    # x = np.arange(len(self.labels))  # the label locations
    # width = 0.35  # the width of the bars

    # fig, ax = plt.subplots()
    # rects1 = ax.bar(x - width/2, men_means, width, label='Men')
    # rects2 = ax.bar(x + width/2, women_means, width, label='Women')
    # rects3 = ax.bar(x + width/2, women_means, width, label='Women')

    # # Add some text for labels, title and custom x-axis tick labels, etc.
    # ax.set_ylabel('Scores')
    # ax.set_title('Scores by group and gender')
    # ax.set_xticks(x)
    # ax.set_xticklabels(labels)
    # ax.legend()

    # fig.tight_layout()

    # plt.show()
    pass


def draw_by_visited(result):
    pass

def draw_by_processed(result):
    pass

def draw_by_depth(result):
    pass

def draw_by_time(result):
    pass


def main():
    # all puzzle arrays will be the same size, 4x4
    correct_puzzle = generate_correct_state()
    Puzzle.correct_state, Puzzle.puzzle_height, Puzzle.puzzle_width = correct_puzzle, 4, 4

    # get all filenames of puzzle files
    list_of_filenames = [[filename for filename in os.listdir("to_draw/") if "4x4_0" + str(i) in filename] for i in range(1, 8)]

    # generate list of all puzzles
    list_of_puzzles = [[load_initial_puzzle(filename) for filename in list_of_filenames[i]] for i in range(7)]   

    # generate list of all first state objects
    list_for_bfs = [[Puzzle(single) for single in single_list] for single_list in list_of_puzzles]
    list_for_dfs = [[Puzzle(single) for single in single_list] for single_list in list_of_puzzles]
    list_for_astr_manh = [[Puzzle(single) for single in single_list] for single_list in list_of_puzzles]

    # generate list of all results for given methods

    # for bfs

    start_time = time.perf_counter()
    res_bfs = [[Bfs(single_state, order).run_search() for order in direction_orders for single_state in single_list ] for single_list in list_for_bfs]
    end_time = time.perf_counter()
    print("BFS generating time: ",end_time - start_time)

    # for dfs

    start_time = time.perf_counter()
    res_dfs = [[Dfs(single_state, order).run_search() for order in direction_orders for single_state in single_list ] for single_list in list_for_dfs]
    end_time = time.perf_counter()
    print("DFS generating time: ",end_time - start_time)

    # for astar, hamm with manh

    start_time = time.perf_counter()
    res_astr = [[Astr(single_state, heuristic).run_search() for heuristic in heuristics for single_state in single_list ] for single_list in list_for_astr_manh]
    end_time = time.perf_counter()
    print("Astr generating time: ",end_time - start_time)

    # CALCULATE MEANS SECTION
    """
    Solution length / Visited states / Processed states / Max depth / execution
    First graph: Means for BFS, DFS, Astar together
    Second graph: Means for BFS orderly separated
    Third graph: Means for DFS orderly separated
    Fourth graph: Means for Astar heuristics separated
    """

    

if __name__ == "__main__":
    main()