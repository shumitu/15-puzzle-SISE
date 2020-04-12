import numpy as np 
import time
from collections import deque
from puzzle import Puzzle

class Bfs:
    def __init__(self, initial_state, search_order):
        super().__init__()

        # popleft() for FIFO / append()
        self.frontier = deque()
        self.already_processed = deque()

        self.frontier.append(initial_state)
        self.search_order = search_order

        self.result_string = ""
        self.max_depth = 0
        self.number_of_visited = 0
        self.number_of_processed = 0

        self.start_time = 0
        self.end_time = 0


    # For every direction in search order generate new states using given state
    def generate_new_states(self, state, search_order):
        for direction in search_order:
            # Call 2 functions to check if move is possible in given direction and if move is not reversed 
            if state.check_if_move_possible(direction) and state.check_if_not_reversed(direction):
                new_state = Puzzle(state.current_state)
                new_state.solution_string = state.solution_string
                new_state.depth = state.depth
                new_state.previous_direction = direction
                new_state.make_move(direction)
                #Add new state to queue
                self.frontier.append(new_state)


    def run_search(self):

        self.start_time = time.perf_counter()

        solution_found = False

        while self.frontier:

            # Get first element from queue, FIFO order
            state_in_queue = self.frontier.popleft()
            self.already_processed.append(state_in_queue)

            # If current state of puzzle is correct, break loop and return result string and additional data
            if state_in_queue.check_if_solved():
                solution_found = True
                self.result_string = state_in_queue.solution_string
                self.max_depth = state_in_queue.depth
                self.number_of_visited = len(self.frontier) + len(self.already_processed)
                self.number_of_processed = len(self.already_processed)
                self.end_time = time.perf_counter()
                break

            # Generate new states using current state and given search order, e.g. LRUD
            self.generate_new_states(state_in_queue, self.search_order)

        # If result was found return result string and other elements
        return self.result_string, self.max_depth, self.number_of_visited, self.number_of_processed, round((self.end_time - self.start_time) * 1000, 3) if solution_found else "No solution found!"

            

    