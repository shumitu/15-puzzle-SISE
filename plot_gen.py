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


labels = ["1", "2", "3", "4", "5", "6", "7"]
direction_orders = ["rdul", "rdlu", "drul", "drlu", "ludr", "lurd", "uldr", "ulrd"]
heuristics = ["manh", "hamm"]


def load_initial_puzzle(filename):
    return np.loadtxt("to_draw/" + filename, dtype=int, skiprows=1)  


def generate_correct_state(height = 4, width = 4):

    correct = np.arange(1, height * width + 1).reshape(height, width)
    correct[height - 1][width - 1] = 0
    return correct


def string_mean(result):
    sum_of_str = [0 for i in range(len(result))]
    no_of_elems = [0 for i in range(len(result))]
    averages = [0 for i in range(len(result))]
    for i in range(len(result)):
        for j in range(len(result[i])):
            sum_of_str[i] += len(result[i][j][0])
            no_of_elems[i] += 1

    for i in range(len(sum_of_str)):
        averages[i] = sum_of_str[i] / no_of_elems[i]

    return averages


def other_mean(result, pos):
    sum_of_str = [0 for i in range(len(result))]
    no_of_elems = [0 for i in range(len(result))]
    averages = [0 for i in range(len(result))]
    for i in range(len(result)):
        for j in range(len(result[i])):
            sum_of_str[i] += result[i][j][pos]
            no_of_elems[i] += 1

    for i in range(len(sum_of_str)):
        averages[i] = sum_of_str[i] / no_of_elems[i]

    return averages


def draw_means_together(bfs, dfs, astr, variant):

    # set width of bar
    barWidth = 0.25
    plt.clf()

    # set height of bar

    if variant == 0:
        bfs_means = string_mean(bfs)
        dfs_means = string_mean(dfs)
        astar_means = string_mean(astr)
        filename = "mean_tog_sol_length.png"
        y_title = "Średnia długość rozwiązania"

    if variant == 1:
        bfs_means = other_mean(bfs, 1)
        dfs_means = other_mean(dfs, 1)
        astar_means = other_mean(astr, 1)
        filename = "mean_tog_num_depth.png"
        y_title = "Średnia maksymalna głębokość rekursji"

    if variant == 2:
        bfs_means = other_mean(bfs, 2)
        dfs_means = other_mean(dfs, 2)
        astar_means = other_mean(astr, 2)
        filename = "mean_tog_num_visited.png"
        y_title = "Średnia liczba odwiedzonych stanów"

    if variant == 3:
        bfs_means = other_mean(bfs, 3)
        dfs_means = other_mean(dfs, 3)
        astar_means = other_mean(astr, 3)
        filename = "mean_tog_num_processed.png"
        y_title = "Średnia liczba przetworzonych stanów"

    if variant == 4:
        bfs_means = other_mean(bfs, 4)
        dfs_means = other_mean(dfs, 4)
        astar_means = other_mean(astr, 4)
        filename = "mean_tog_exec_time.png"
        y_title = "Średni czas wykonania [ms]"

    
    # Set position of bar on X axis
    r1 = np.arange(len(bfs_means))
    r2 = [x + barWidth for x in r1]
    r3 = [x + barWidth for x in r2]
    
    # Make the plot
    plt.bar(r1, bfs_means, color='#172d9a', width=barWidth, edgecolor='white', label='BFS')
    plt.bar(r2, dfs_means, color='#28892a', width=barWidth, edgecolor='white', label='DFS')
    plt.bar(r3, astar_means, color='#ad4509', width=barWidth, edgecolor='white', label='A*')
    
    # Add xticks on the middle of the group bars
    plt.title("Ogółem", fontweight="bold", loc="center")
    plt.xlabel("Głębokość", fontweight="bold")
    plt.ylabel(y_title, fontweight="bold")
    plt.xticks([r + barWidth for r in range(len(bfs_means))], labels)
    
    # Create legend & Show graphic
    plt.legend()
    plt.savefig("plots/" + filename, dpi=300)



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

    # CALCULATE AND PLOT SECTION
    """
    Solution length / Visited states / Processed states / Max depth / execution, together 20 graphs
    First graph: Means for BFS, DFS, Astar together
    Second graph: Means for BFS orderly separated
    Third graph: Means for DFS orderly separated
    Fourth graph: Means for Astar heuristics separated
    """

    # DRAW MEANS FOR SOLUTION LENGTH TOGETHER
    draw_means_together(res_bfs,res_dfs,res_astr, 0)
    draw_means_together(res_bfs,res_dfs,res_astr, 1)
    draw_means_together(res_bfs,res_dfs,res_astr, 2)
    draw_means_together(res_bfs,res_dfs,res_astr, 3)
    draw_means_together(res_bfs,res_dfs,res_astr, 4)



if __name__ == "__main__":
    main()