import numpy as np 
from collections import deque
import time
from queue import PriorityQueue
from puzzle import Puzzle

class Astr:
    def __init__(self, initial_state, heuristic):
        self.heuristic = heuristic
        self.frontier = PriorityQueue()
        self.already_processed = {}

        self.frontier.put((0, initial_state))

        self.solution_found = False

        self.result_string = ""
        self.max_depth = 0
        self.number_of_visited = 1
        self.number_of_processed = 0

        self.start_time = 0
        self.end_time = 0
    

    # Function to calculate hamming distance which is number of misplaced tiles, without '0' which is an empty tile 
    def hamming_dist(self, state):
        distance = 0
        for i in range(Puzzle.puzzle_width):
            for j in range(Puzzle.puzzle_height):
                if state.current_state[i][j] != state.correct_state[i][j] and state.current_state[i][j] != 0:
                    distance += 1
        
        return distance


    # Function to calculate manhattan distance which is sum of distances of every mispleaced tile to it correct position, without '0' which is an empty tile 
    def manhattan_dist(self, state):
        distance = 0
        for i in range(Puzzle.puzzle_width):
            for j in range(Puzzle.puzzle_height):
                val = state.current_state[i][j] # i - row, j - column
                if val != 0:
                    val -= 1
                    new_x = val % Puzzle.puzzle_width
                    new_y = val // Puzzle.puzzle_height

                    # Take the sum of the absolute values of the differences of the coordinates.
                    distance += abs(i - new_y) + abs(j - new_x)

        return distance


    def choose_heuristic(self, state, heuristic):
        switch_by_heuristic = {
            "manh": self.manhattan_dist,
            "hamm": self.hamming_dist
        }
        result = switch_by_heuristic.get(heuristic.lower(), "Wrong heuristic!") 
        return result(state) if type(result) is not str else print(result)


    # Generate new states using given state
    def generate_new_states(self, state, search_order = "rdlu"):
        for direction in search_order:
            if state.check_if_move_possible(direction) and state.check_if_not_reversed(direction):
                new_state = Puzzle(state.current_state)
                new_state.solution_string = state.solution_string
                new_state.depth = state.depth
                new_state.previous_direction = direction
                new_state.make_move(direction)

                if new_state.check_if_solved():
                    self.result_string = new_state.solution_string
                    self.max_depth = new_state.depth
                    self.end_time = time.perf_counter()
                    self.solution_found = True

                else:  
                    # Calculate cost of movements and add this value with new state to priority queue
                    heuristic_val = new_state.depth + self.choose_heuristic(new_state, self.heuristic)
                    self.frontier.put((heuristic_val, new_state))
                    self.number_of_visited += 1
               

    # Function to generate hash of puzzle for given state
    def generate_hash(self, state):
        return hash(state.current_state.tobytes())


    def run_search(self):
        
        self.start_time = time.perf_counter()

        while self.frontier and not self.solution_found:

            # Get state from priority queue for which value of priority is the lowest
            # Priority queue  returns tuple (priority, state), so we take [1] to get only state
            state_in_queue = self.frontier.get()[1]

            if self.generate_hash(state_in_queue) in self.already_processed:
                state_in_queue = self.frontier.get()[1]
                self.number_of_visited += 1

            self.generate_new_states(state_in_queue)
            self.already_processed[self.generate_hash(state_in_queue)] = state_in_queue.depth
            self.number_of_processed += 1

        return self.result_string, self.max_depth, self.number_of_visited, self.number_of_processed, round((self.end_time - self.start_time) * 1000, 3) if self.solution_found else "No solution found!"
        



            



