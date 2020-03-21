import numpy as np 
from collections import deque

class Puzzle(object):
    
    correct_state = None
    puzzle_height = int 
    puzzle_width = int

    def __init__(self, current_state):
        super().__init__()

        self.current_state = np.copy(current_state)



        # return tuple (y, x)
        self.zero_index = np.argwhere(self.current_state == 0)[0]

        self.solution_string = ""
        self.current_direction = ""
        self.depth = 0 


    def check_if_solved(self):
        return (self.current_state == self.correct_state).all()

        
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


    def down(self):
        self.current_state[self.zero_index[0]][self.zero_index[1]], self.current_state[self.zero_index[0] + 1][self.zero_index[1]] = self.current_state[self.zero_index[0] + 1][self.zero_index[1]], self.current_state[self.zero_index[0]][self.zero_index[1]]
        self.zero_index[0] += 1
        self.solution_string += "d"
        self.depth += 1


    def up(self):
        self.current_state[self.zero_index[0]][self.zero_index[1]], self.current_state[self.zero_index[0] - 1][self.zero_index[1]] = self.current_state[self.zero_index[0] - 1][self.zero_index[1]], self.current_state[self.zero_index[0]][self.zero_index[1]]
        self.zero_index[0] -= 1
        self.solution_string += "u"
        self.depth += 1


    def left(self):
        self.current_state[self.zero_index[0]][self.zero_index[1]], self.current_state[self.zero_index[0]][self.zero_index[1] - 1] = self.current_state[self.zero_index[0]][self.zero_index[1] - 1], self.current_state[self.zero_index[0]][self.zero_index[1]]
        self.zero_index[1] -= 1
        self.solution_string += "l"
        self.depth += 1
        

    def right(self):
        self.current_state[self.zero_index[0]][self.zero_index[1]], self.current_state[self.zero_index[0]][self.zero_index[1] + 1] = self.current_state[self.zero_index[0]][self.zero_index[1] + 1], self.current_state[self.zero_index[0]][self.zero_index[1]]    
        self.zero_index[1] += 1 
        self.solution_string += "r"
        self.depth += 1

    def make_move(self,direction):
        switch_by_direction = {
            'd': self.down,
            'l': self.left,
            'u': self.up,
            'r': self.right
        }
        result = switch_by_direction.get(direction.lower(), "Wrong direction!")
        return result()