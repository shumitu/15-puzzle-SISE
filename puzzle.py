import numpy as np 
from collections import deque

class Puzzle:
    
    #Default values for 4x4 puzzle
    correct_state = np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]])
    puzzle_height = 4 
    puzzle_width = 4

    def __init__(self, current_state):
        self.current_state = np.copy(current_state)

        # return tuple (y, x)
        self.zero_index = np.argwhere(self.current_state == 0)[0]

        self.solution_string = ""
        self.current_direction = ""
        self.previous_direction = ""
        self.depth = 0 


    def __lt__(self, other):
        return self.depth < other.depth


    def __le__(self, other):
        return not other.depth < self.depth
        

    def check_if_solved(self):
        return self.current_state.tobytes() == self.correct_state.tobytes()

    
    # Function which check if move in given direction is possible
    def check_if_move_possible(self, direction):
        if direction not in 'urdl':
            return False
        if self.zero_index[0] == 0 and direction == 'u':
            return False
        if self.zero_index[0] == self.puzzle_height - 1 and direction == 'd':
            return False
        if self.zero_index[1] == 0 and direction == 'l':
            return False
        if self.zero_index[1] == self.puzzle_width - 1 and direction == 'r':
            return False
        return True


    # Function which check if given direction is not opposite to previous direction
    def check_if_not_reversed(self, direction):
        if self.previous_direction == 'u' and direction == 'd':
            return False
        if self.previous_direction == 'd' and direction == 'u':
            return False
        if self.previous_direction == 'l' and direction == 'r':
            return False
        if self.previous_direction == 'r' and direction == 'l':
            return False    
        return True


    def down(self):
        self.current_state[self.zero_index[0]][self.zero_index[1]], self.current_state[self.zero_index[0] + 1][self.zero_index[1]] = (
            self.current_state[self.zero_index[0] + 1][self.zero_index[1]], self.current_state[self.zero_index[0]][self.zero_index[1]])
        
        self.zero_index[0] += 1
        self.solution_string += "d"
        self.depth += 1


    def up(self):
        self.current_state[self.zero_index[0]][self.zero_index[1]], self.current_state[self.zero_index[0] - 1][self.zero_index[1]] = (
            self.current_state[self.zero_index[0] - 1][self.zero_index[1]], self.current_state[self.zero_index[0]][self.zero_index[1]])

        self.zero_index[0] -= 1
        self.solution_string += "u"
        self.depth += 1


    def left(self):
        self.current_state[self.zero_index[0]][self.zero_index[1]], self.current_state[self.zero_index[0]][self.zero_index[1] - 1] = (
            self.current_state[self.zero_index[0]][self.zero_index[1] - 1], self.current_state[self.zero_index[0]][self.zero_index[1]])
        
        self.zero_index[1] -= 1
        self.solution_string += "l"
        self.depth += 1
        

    def right(self):
        self.current_state[self.zero_index[0]][self.zero_index[1]], self.current_state[self.zero_index[0]][self.zero_index[1] + 1] = (
            self.current_state[self.zero_index[0]][self.zero_index[1] + 1], self.current_state[self.zero_index[0]][self.zero_index[1]])
                
        self.zero_index[1] += 1 
        self.solution_string += "r"
        self.depth += 1


    # Function which acts like switch ... case
    def make_move(self,direction):
        switch_by_direction = {
            'd': self.down,
            'l': self.left,
            'u': self.up,
            'r': self.right
        }
        result = switch_by_direction.get(direction.lower(), "Wrong direction!")
        return result() if type(result) is not str else print(result)