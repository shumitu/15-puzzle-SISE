import numpy as np 
import time
from collections import deque
from puzzle import Puzzle

class Dfs:

    #Default value for university classess
    max_depth_possible = 20
    
    def __init__(self, initial_state, search_order):
        # pop() for LIFO / append()
        self.frontier = deque()
        self.already_processed = {}
        
        # Add first state to frontier
        self.frontier.append(initial_state)

        self.search_order = search_order
        self.result_string = ""
        self.max_depth = 0
        self.number_of_visited = 0
        self.number_of_processed = 0

        self.solution_found = False

        self.start_time = 0
        self.end_time = 0


    # Function to generate hash of puzzle for given state
    def generate_hash(self, state):
        return hash(state.current_state.tobytes())


    # For every direction in search order generate new states using given state
    def generate_new_states(self, state, search_order):
        to_reverse = []
        for direction in search_order:

            # Check if move is possible in given direction and if depth is lower than max possible depth
            if state.check_if_move_possible(direction) and state.check_if_not_reversed(direction) and state.depth < self.max_depth_possible:
                new_state = Puzzle(state.current_state)
                new_state.solution_string = state.solution_string
                new_state.depth = state.depth
                new_state.previous_direction = direction
                new_state.make_move(direction)

                # If new state is solved, we set params and flag to true
                if new_state.check_if_solved():
                    self.result_string = new_state.solution_string
                    self.max_depth = new_state.depth
                    self.end_time = time.perf_counter()
                    self.solution_found = True

                else:
                    to_reverse.append(new_state)
        
        to_reverse.reverse()
        for single in to_reverse:
            self.frontier.append(single)
            self.number_of_visited += 1


    def run_search(self):
        
        self.start_time = time.perf_counter()
    
        while self.frontier and not self.solution_found:

            # Get first element from queue, LIFO order
            state_in_queue = self.frontier.pop()

            if state_in_queue.depth > self.max_depth_possible:
                continue

            # Check if given state was already visited using hash and dict
            if self.generate_hash(state_in_queue) in self.already_processed:

                if state_in_queue.depth >= self.already_processed[self.generate_hash(state_in_queue)]:
                    continue

            # Add new state to dict using hash of object, generate new states
            self.generate_new_states(state_in_queue, self.search_order)
            self.already_processed[self.generate_hash(state_in_queue)] = state_in_queue.depth
            self.number_of_processed += 1

        # If result was found return result string and other elements
        return self.result_string, self.max_depth, self.number_of_visited, self.number_of_processed, round((self.end_time - self.start_time) * 1000, 3) if self.solution_found else "No solution found!"
                
        




