import numpy as np 
from collections import deque
from puzzle import Puzzle

class Bfs(object):
    def __init__(self, initial_state, search_order):
        super().__init__()

        self.to_be_visited = deque()
        self.already_visited = deque()

        self.to_be_visited.append(initial_state)
        self.search_order = search_order

        self.result_string = ""
        self.max_depth = 0
        self.number_of_visited = 0
        self.number_of_processed = 0


    def generate_new_states(self, state, search_order):
        for direction in search_order:
            if state.check_if_move_possible(direction) and state.check_if_not_reversed(direction):
                new_state = Puzzle(state.current_state)
                new_state.solution_string = state.solution_string
                new_state.depth = state.depth
                new_state.previous_direction = direction
                new_state.make_move(direction)
                self.to_be_visited.append(new_state)


    def run_search(self):

        solution_found = False

        while self.to_be_visited:

            state_in_queue = self.to_be_visited.popleft()
            self.already_visited.append(state_in_queue)

            if state_in_queue.check_if_solved():
                solution_found = True
                self.result_string = state_in_queue.solution_string
                self.max_depth = state_in_queue.depth
                self.number_of_visited = len(self.to_be_visited) + len(self.already_visited)
                self.number_of_processed = len(self.already_visited)
                break

            self.generate_new_states(state_in_queue, self.search_order)

        return self.result_string, self.max_depth, self.number_of_visited, self.number_of_processed if solution_found else "No solution found!"

            

    