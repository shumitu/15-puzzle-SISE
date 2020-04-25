import sys
import time
import os
import random
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

from puzzle import Puzzle
from bfs import Bfs
from dfs import Dfs
from astr import Astr

#Initial arrays of depth labels, search orders, heursitics and colors used in plots
labels = ["1", "2", "3", "4", "5", "6", "7"]
direction_orders = ["rdul", "rdlu", "drul", "drlu", "ludr", "lurd", "uldr", "ulrd"]
heuristics = ["manh", "hamm"]
colors = ["firebrick", "navy", "green", "darkorange", "black", "darkcyan", "lawngreen", "purple"]


#Load initial puzzles from files
def load_initial_puzzle(filename):
    return np.loadtxt("to_draw/" + filename, dtype = int, skiprows = 1)  


#Generate correct state for given size. Default variant is 4x4
def generate_correct_state(height = 4, width = 4):
    correct = np.arange(1, height * width + 1).reshape(height, width)
    correct[height - 1][width - 1] = 0
    return correct


#Ugly function to calculate means of solutions in form of strings
def string_mean(result, separated, method = "empty"):
    if not separated:
        sum_of_str = [0 for _ in range(len(result))]
        no_of_elems = [0 for _ in range(len(result))]
        averages = [0 for _ in range(len(result))]
        for i in range(len(result)):
            for j in range(len(result[i])):
                sum_of_str[i] += len(result[i][j][0][0])
                no_of_elems[i] += 1

        for i in range(len(sum_of_str)):
            averages[i] = sum_of_str[i] / no_of_elems[i]

        return averages

    else:
        # create list of dictionaries and declare values for orders or heuristics as lists or 0
        list_of_dicts = [{} for _ in range(len(result))]
        list_of_sums = [{} for _ in range(len(result))]
        list_of_elem_sums = [{} for _ in range(len(result))]
        list_of_averages = [{} for _ in range(len(result))]

        for single_dict in list_of_dicts:
            for order in direction_orders if method == "empty" else heuristics:
                single_dict[order] = []
        
        for single_dict in list_of_sums:
            for order in direction_orders if method == "empty" else heuristics:
                single_dict[order] = 0
        
        for single_dict in list_of_elem_sums:
            for order in direction_orders if method == "empty" else heuristics:
                single_dict[order] = 0

        for single_dict in list_of_averages:
            for order in direction_orders if method == "empty" else heuristics:
                single_dict[order] = 0
    
        # separate data via orders or heuristics
        for order in direction_orders if method == "empty" else heuristics:
            for i in range(len(result)):
                for j in range(len(result[i])):
                    if result[i][j][1] == order:
                        list_of_dicts[i][order].append(result[i][j][0])

        # calculate length for strings
        for order in direction_orders if method == "empty" else heuristics:
            for i in range(len(result)):
                for j in range(len(list_of_dicts[i][order])):
                    list_of_sums[i][order] += len(list_of_dicts[i][order][j][0])
                    list_of_elem_sums[i][order] += 1

        for order in direction_orders if method == "empty" else heuristics:
            for i in range(len(list_of_sums)):
                list_of_averages[i][order] = list_of_sums[i][order] / list_of_elem_sums[i][order]

        return list_of_averages


#Calculate means for values that are not strings
def other_mean(result, pos, separated, method = "empty"):
    if not separated:
        sum_of_str = [0 for i in range(len(result))]
        no_of_elems = [0 for i in range(len(result))]
        averages = [0 for i in range(len(result))]
        for i in range(len(result)):
            for j in range(len(result[i])):
                sum_of_str[i] += result[i][j][0][pos]
                no_of_elems[i] += 1

        for i in range(len(sum_of_str)):
            averages[i] = sum_of_str[i] / no_of_elems[i]

        return averages

    else:
        # create list of dictionaries and declare values for orders as lists or 0
        list_of_dicts = [{} for _ in range(len(result))]
        list_of_sums = [{} for _ in range(len(result))]
        list_of_elem_sums = [{} for _ in range(len(result))]
        list_of_averages = [{} for _ in range(len(result))]

        for single_dict in list_of_dicts:
            for order in direction_orders if method == "empty" else heuristics:
                single_dict[order] = []
        
        for single_dict in list_of_sums:
            for order in direction_orders if method == "empty" else heuristics:
                single_dict[order] = 0
        
        for single_dict in list_of_elem_sums:
            for order in direction_orders if method == "empty" else heuristics:
                single_dict[order] = 0

        for single_dict in list_of_averages:
            for order in direction_orders if method == "empty" else heuristics:
                single_dict[order] = 0
    
        # separate data via orders
        for order in direction_orders if method == "empty" else heuristics:
            for i in range(len(result)):
                for j in range(len(result[i])):
                    if result[i][j][1] == order:
                        list_of_dicts[i][order].append(result[i][j][0])

        # calculate length
        for order in direction_orders if method == "empty" else heuristics:
            for i in range(len(result)):
                for j in range(len(list_of_dicts[i][order])):
                    list_of_sums[i][order] += list_of_dicts[i][order][j][pos]
                    list_of_elem_sums[i][order] += 1

        for order in direction_orders if method == "empty" else heuristics:
            for i in range(len(list_of_sums)):
                list_of_averages[i][order] = list_of_sums[i][order] / list_of_elem_sums[i][order]

        return list_of_averages


#Function used for drawing plots for not separated data
def draw_means_together(bfs, dfs, astr, variant):

    #set width of bar
    barWidth = 0.25
    plt.clf()

    if variant == 0:
        bfs_means = string_mean(bfs, False)
        dfs_means = string_mean(dfs, False)
        astar_means = string_mean(astr, False)
        filename = "mean_together_solution_length.png"
        y_title = "Średnia długość rozwiązania"

    if variant == 1:
        bfs_means = other_mean(bfs, 1, False)
        dfs_means = other_mean(dfs, 1, False)
        astar_means = other_mean(astr, 1, False)
        filename = "mean_together_max_depth.png"
        y_title = "Średnia maksymalna głębokość rekursji"

    if variant == 2:
        bfs_means = other_mean(bfs, 2, False)
        dfs_means = other_mean(dfs, 2, False)
        astar_means = other_mean(astr, 2, False)
        filename = "mean_together_number_visited.png"
        y_title = "Średnia liczba odwiedzonych stanów"
        plt.yscale("log", subsy=[2, 4, 6, 8])

    if variant == 3:
        bfs_means = other_mean(bfs, 3, False)
        dfs_means = other_mean(dfs, 3, False)
        astar_means = other_mean(astr, 3, False)
        filename = "mean_together_number_processed.png"
        y_title = "Średnia liczba przetworzonych stanów"
        plt.yscale("log", subsy=[2, 4, 6, 8])

    if variant == 4:
        bfs_means = other_mean(bfs, 4, False)
        dfs_means = other_mean(dfs, 4, False)
        astar_means = other_mean(astr, 4, False)
        filename = "mean_togerher_execution_time.png"
        y_title = "Średni czas wykonania [ms]"
        plt.yscale("log", subsy=[2, 4, 6, 8])

    #Set position of bar on X axis
    r1 = np.arange(len(bfs_means))
    r2 = [x + barWidth for x in r1]
    r3 = [x + barWidth for x in r2]
    
    #Make the plot
    plt.bar(r1, bfs_means, color=colors[0], width=barWidth, edgecolor='black', linewidth=1, label='BFS')
    plt.bar(r2, dfs_means, color=colors[1], width=barWidth, edgecolor='black', linewidth=1,label='DFS')
    plt.bar(r3, astar_means, color=colors[2], width=barWidth, edgecolor='black', linewidth=1, label='A*')
    
    #Add xticks on the middle of the group bars
    plt.title("Ogółem", fontweight="bold", loc="center")
    plt.xlabel("Głębokość", fontweight="bold")
    plt.ylabel(y_title, fontweight="bold")
    plt.xticks([r + barWidth for r in range(len(bfs_means))], labels)
    
    # Create legend and save plot to file
    plt.legend()
    plt.savefig("plots/" + filename, dpi=300)


#Function used for drawing plots for separated data
def draw_separated(plot_data, method, variant):

    plt.clf()

    if variant == 0:
        method_means = string_mean(plot_data, True,method) if method == "astr" else string_mean(plot_data, True)
        filename = "mean_" + method + "_separated_solution_length.png"
        y_title = "Średnia długość rozwiązania"
        x_title = "A*" if method == "astr" else method.upper()

    if variant == 1:
        method_means = other_mean(plot_data, 1, True,method) if method == "astr" else other_mean(plot_data, 1, True)
        filename = "mean_" + method + "_separated_max_depth.png"
        y_title = "Średnia maksymalna głębokość rekursji"
        x_title = "A*" if method == "astr" else method.upper()

    if variant == 2:
        method_means = other_mean(plot_data, 2, True,method) if method == "astr" else other_mean(plot_data, 2, True)
        filename = "mean_" + method + "_separated_number_visited.png"
        y_title = "Średnia liczba odwiedzonych stanów"
        x_title = "A*" if method == "astr" else method.upper()
        if method == "dfs": plt.yscale("log", subsy=[2, 4, 6, 8])

    if variant == 3:
        method_means = other_mean(plot_data, 3, True,method) if method == "astr" else other_mean(plot_data, 3, True)
        filename = "mean_" + method + "_separated_number_processed.png"
        y_title = "Średnia liczba przetworzonych stanów"
        x_title = "A*" if method == "astr" else method.upper()
        if method == "dfs": plt.yscale("log", subsy=[2, 4, 6, 8])

    if variant == 4:
        method_means = other_mean(plot_data, 4, True,method) if method == "astr" else other_mean(plot_data, 4, True)
        filename = "mean_" + method + "_separated_exec_time.png"
        y_title = "Średni czas wykonania [ms]"
        x_title = "A*" if method == "astr" else method.upper()
        if method == "dfs": plt.yscale("log", subsy=[2, 4, 6, 8])

    if method == "astr":
        barWidth = 0.45
        r1 = np.arange(len(method_means))
        r2 = [x + barWidth for x in r1]
        out_1 = [method[heuristics[0]] for method in method_means]
        out_2 = [method[heuristics[1]] for method in method_means]
        plt.bar(r1, out_1, color=colors[0], width=barWidth, edgecolor='black', linewidth=1, label=heuristics[0])
        plt.bar(r2, out_2, color=colors[1], width=barWidth, edgecolor='black', linewidth=1, label=heuristics[1])
        plt.xticks([r + barWidth / 2 for r in range(len(out_1))], labels)

    else:
        barWidth = 0.10

        r1 = np.arange(len(method_means))
        r2 = [x + barWidth for x in r1] 
        r3 = [x + barWidth for x in r2]
        r4 = [x + barWidth for x in r3]
        r5 = [x + barWidth for x in r4]
        r6 = [x + barWidth for x in r5]
        r7 = [x + barWidth for x in r6]
        r8 = [x + barWidth for x in r7]

        out_1 = [method[direction_orders[0]] for method in method_means]
        out_2 = [method[direction_orders[1]] for method in method_means]
        out_3 = [method[direction_orders[2]] for method in method_means]
        out_4 = [method[direction_orders[3]] for method in method_means]
        out_5 = [method[direction_orders[4]] for method in method_means]
        out_6 = [method[direction_orders[5]] for method in method_means]
        out_7 = [method[direction_orders[6]] for method in method_means]
        out_8 = [method[direction_orders[7]] for method in method_means]

        plt.bar(r1, out_1, color=colors[0], width=barWidth, edgecolor='black', linewidth=1, label=direction_orders[0])
        plt.bar(r2, out_2, color=colors[1], width=barWidth, edgecolor='black', linewidth=1, label=direction_orders[1])
        plt.bar(r3, out_3, color=colors[2], width=barWidth, edgecolor='black', linewidth=1, label=direction_orders[2])
        plt.bar(r4, out_4, color=colors[3], width=barWidth, edgecolor='black', linewidth=1, label=direction_orders[3])
        plt.bar(r5, out_5, color=colors[4], width=barWidth, edgecolor='black', linewidth=1, label=direction_orders[4])
        plt.bar(r6, out_6, color=colors[5], width=barWidth, edgecolor='black', linewidth=1, label=direction_orders[5])
        plt.bar(r7, out_7, color=colors[6], width=barWidth, edgecolor='black', linewidth=1, label=direction_orders[6])
        plt.bar(r8, out_8, color=colors[7], width=barWidth, edgecolor='black', linewidth=1, label=direction_orders[7])

        plt.xticks([r + 3 * barWidth for r in range(len(out_1))], labels)
    
    # Add xticks on the middle of the group bars
    plt.title(x_title, fontweight="bold", loc="center")
    plt.xlabel("Głębokość", fontweight="bold")
    plt.ylabel(y_title, fontweight="bold")
    
    # Create legend and save plot to file
    plt.legend(ncol=2, fontsize="small")
    plt.savefig("plots/" + filename, dpi=300)

# Simple functions which is used in multiprocessing
def dfs_worker(single_list):
    res_dfs = [(Dfs(single_state, order).run_search(), order) for order in direction_orders for single_state in single_list]
    return res_dfs


def bfs_worker(single_list):
    res_bfs = [(Bfs(single_state, order).run_search(), order) for order in direction_orders for single_state in single_list]
    return res_bfs


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
    res_bfs = [[(Bfs(single_state, order).run_search(), order) for order in direction_orders for single_state in single_list ] for single_list in list_for_bfs]
    end_time = time.perf_counter()
    print("BFS generating time: ",round(end_time - start_time, 3), "s")

    # for dfs

    start_time = time.perf_counter()
    executors_list_dfs = []
    with ProcessPoolExecutor(max_workers = 3) as executor:
        for i in range(len(list_for_dfs)):
            executors_list_dfs.append(executor.submit(dfs_worker, list_for_dfs[i]))
    end_time = time.perf_counter()
    res_dfs = [i.result() for i in executors_list_dfs]

    print("DFS generating time: ",round(end_time - start_time, 3), "s" ,round((end_time - start_time) / 3600, 3), "h" )

    # for astar, hamm with manh

    start_time = time.perf_counter()
    res_astr = [[(Astr(single_state, heuristic).run_search(), heuristic) for heuristic in heuristics for single_state in single_list ] for single_list in list_for_astr_manh]
    end_time = time.perf_counter()
    print("Astr generating time: ",round(end_time - start_time, 3), "s")

    # Section for plots generating process
    """
    Solution length / Visited states / Processed states / Max depth / execution, together 20 graphs
    First graph: Means for BFS, DFS, Astar together
    Second graph: Means for BFS orderly separated
    Third graph: Means for DFS orderly separated
    Fourth graph: Means for Astar heuristics separated
    """

    # Draw means plots for results together
    for i in range(5):
        draw_means_together(res_bfs,res_dfs,res_astr, i)
        draw_separated(res_bfs, "bfs", i)
        draw_separated(res_dfs, "dfs", i)
        draw_separated(res_astr, "astr", i)
        

if __name__ == "__main__":
    main()