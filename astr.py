import numpy as np 
from collections import deque
from queue import PriorityQueue
from puzzle import Puzzle

class Astr(object):
    def __init__(self, initial_state, heuristic):
        super().__init__()

        self.heuristic = heuristic
        self.to_be_visited = PriorityQueue()
        self.already_vistied = deque()

        self.to_be_visited.put((0, initial_state))

        self.result_string = ""
        self.max_depth = 0
        self.number_of_visited = 0
    

    def hamming_dist(self, state):
        distance = 0
        for i in range(Puzzle.puzzle_width):
            for j in range(Puzzle.puzzle_height):
                if state.current_state[i][j] != state.correct_state[i][j] and state.current_state[i][j] != 0:
                    distance += 1
        
        return distance


    def manhattan_dist(self, state):
        distance = 0
        for i in range(Puzzle.puzzle_width):
            for j in range(Puzzle.puzzle_height):
                val = state.current_state[i][j]
                if val != 0:
                    val -= 1
                    new_x = val % Puzzle.puzzle_width
                    new_y = val // Puzzle.puzzle_height

                    distance += abs(i - new_y) + abs(j - new_x)

        return distance


    def choose_heuristic(self, state, heuristic):
        switch_by_heuristic = {
            "manh": self.manhattan_dist,
            "hamm": self.hamming_dist
        }
        result = switch_by_heuristic.get(heuristic.lower(), "Wrong heuristic!")
        return result(state)


    def generate_new_states(self, state, search_order = "lurd"):
        for direction in search_order:
            if state.check_if_move_possible(direction) and state.check_if_not_reversed(direction):
                new_state = Puzzle(state.current_state)
                new_state.solution_string = state.solution_string
                new_state.depth = state.depth
                new_state.previous_direction = direction
                new_state.make_move(direction)
                
                heuristic_val = new_state.depth + self.choose_heuristic(new_state, self.heuristic)
                self.to_be_visited.put((heuristic_val, new_state))
               


    def check_if_new(self, dict_of_states, state_to_check):

        if state_to_check in dict_of_states:
            return False

        else:
            return True


    def run_search(self):

        solution_found = False

        while self.to_be_visited:

            state_in_queue = self.to_be_visited.get()[1]

            if self.already_vistied:

                while not self.check_if_new(self.already_vistied, state_in_queue):
                    state_in_queue = self.to_be_visited.get()[1]

            if state_in_queue.depth > self.max_depth:
                self.max_depth = state_in_queue.depth

            if state_in_queue.check_if_solved():
                solution_found = True
                self.result_string = state_in_queue.solution_string
                self.max_depth = state_in_queue.depth
                self.number_of_visited = len(self.already_vistied)
                break

            self.generate_new_states(state_in_queue)

            self.already_vistied.append(state_in_queue)

        return self.result_string, self.max_depth, self.number_of_visited if solution_found else "No solution found!"
        



            



