import numpy as np 
from collections import deque
from puzzle import Puzzle

class Dfs(object):

    max_depth_possible = 15
    
    def __init__(self, initial_state, search_order):
        super().__init__()

        # pop() for LIFO / append()
        self.to_be_visited = deque()
        self.already_vistied = {}

        self.to_be_visited.append(initial_state)

        self.search_order = search_order

        self.result_string = ""
        self.max_depth = 0
        self.number_of_visited = 1
        self.number_of_processed = 0


    # For every direction in search order generate new states using given state
    def generate_new_states(self, state, search_order):
        for direction in search_order:
            if state.check_if_move_possible(direction) and state.check_if_not_reversed(direction):
                new_state = Puzzle(state.current_state)
                new_state.solution_string = state.solution_string
                new_state.depth = state.depth + 1
                new_state.previous_direction = direction
                new_state.make_move(direction)

                self.to_be_visited.append(new_state)
                self.number_of_visited += 1


    def run_search(self):

        solution_found = False
    
        while self.to_be_visited:


            # Get first element from queue, LIFO order
            state_in_queue = self.to_be_visited.pop()

            if state_in_queue.depth > self.max_depth:
                self.max_depth = state_in_queue.depth

            # If current state of puzzle is correct, return result string and additional data
            if state_in_queue.check_if_solved():
                solution_found = True
                self.result_string = state_in_queue.solution_string
                self.max_depth = state_in_queue.depth
                

            else:

                if state_in_queue.depth > self.max_depth_possible:
                    continue

                # Check if given state was already visited using hash and dict
                if hash(state_in_queue) in self.already_vistied:

                    if state_in_queue.depth >= self.already_vistied[hash(state_in_queue)].depth:
                        continue
                    else:
                        del self.already_vistied[hash(state_in_queue)]

                # Add new state to dict using hash of object, generate new states
                self.already_vistied[hash(state_in_queue)] = state_in_queue
                self.generate_new_states(state_in_queue, self.search_order)

        self.number_of_processed = len(self.already_vistied)

        # If result was found return result string and other elements
        return self.result_string, self.max_depth, self.number_of_visited, self.number_of_processed if solution_found else "No solution found!"
                
        




