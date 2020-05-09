import math
import sys
import random
from enum import Enum

'''
HW 4 for CISC681
@author: sfreaney@udel.edu
@updated: 5/08/2020
Uses Q-learning algorithm to determine the best path to a goal state
'''

# Constants
LIVING_REWARD = -0.1
DISCOUNT_RATE = 0.2 #GAMMA
LEARNING_RATE = 0.1
GOAL_REWARD = 100
FORBIDDEN = -100
EPSILON = 0.1 # Probability for random action
MAX_ITERATIONS = 10000 # Will be 10,000
START_LABEL = 2

LEFT = '\u2190'
UP = '\u2191'
RIGHT = '\u2192'
DOWN = '\u2193'

'''
NOTE: All representations of directions in arrays (such as in actions, neighbors, q_values)
will be represented numerically in the same order, clockwise, starting with LEFT
This is shown in the ENUM class - can remember using acronym "L.U.R.D."
s
alpha
s_prime
alpha_prime
gamma
Q(s,alpha) <-- (1-alpha)*Q(s,alpha) + alpha*(R(s,alpha,s_prime) + [gamma * max_over_a_prime(Qk(s_prime,alpha_prime)))]

1. two-digit precision for convergence
2. set epsilon to 0 after convergence

Active reinforcement learning
S = set of states
A = set of actions per state
T(s,a,s') = model of transitions
R(s,a,s') = reward function
pi(s) = policy
don't know T or R
Q0(s,a,) = 0
state - current loc, prev loc, visual scope
'''
class Direction(Enum):
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3
    
    def __str__(self):
        if self.value == 0:
            return '\u2190'
        elif self.value == 1:
            return '\u2191'
        elif self.value == 2:
            return '\u2192'
        elif self.value == 3:
            return '\u2191'
        else:
            return "error printing direction"

class Tile:
    
    def __init__(self, label, neighbors):
        '''
        Attributes:
            label (int): index of tile in visual representation of grid (1-16)
            neighbors (list[int]): labels of neighboring tiles in grid, in order [left,up,right,down]
        '''
        self.label = label
        self.neighbors = neighbors
        self.q_values = [0.00]*4
        # Default values, changed in board creation
        self.goal = False
        self.forbidden = False

    
    def update_q(self, q, direction):
        self.q_values[direction.value] = q
    
    def __str__(self):
        return str(Direction.LEFT) + str(self.q_values[0]) + '|' + str(Direction.UP) + str(self.q_values[1]) + '|' + str(Direction.RIGHT) + str(self.q_values[2]) + '|'  + str(Direction.DOWN) + str(self.q_values[3])

class Board:

    def __init__(self, input_list):
        self.tiles = [[1]*4 for n in range(4)]
        # tiles[row][col]
        # max_row = height - 1
        # max_col = width - 1
        # Neighbors are in order left, up, right, down
        self.tiles[0][0] = Tile(1,[None,5,2,None])
        self.tiles[0][1] = Tile(START_LABEL,[1,6,3,None])
        self.tiles[0][2] = Tile(3,[2,7,4,None])
        self.tiles[0][3] = Tile(4,[3,8,None,None])

        self.tiles[1][0] = Tile(5,[None,9,6,1])
        self.tiles[1][1] = Tile(6,[5,10,7,2])
        self.tiles[1][2] = Tile(7,[6,11,8,3])
        self.tiles[1][3] = Tile(8,[7,12,None,4])

        self.tiles[2][0] = Tile(9,[None,13,10,5])
        self.tiles[2][1] = Tile(10,[9,14,11,6])
        self.tiles[2][2] = Tile(11,[10,15,12,7])
        self.tiles[2][3] = Tile(12,[11,16,None,8])

        self.tiles[3][0] = Tile(13,[None,None,14,9])
        self.tiles[3][1] = Tile(14,[13,None,15,10])
        self.tiles[3][2] = Tile(15,[14,None,16,11])
        self.tiles[3][3] = Tile(16,[15,None,None,12])

        self.iterations = 0

        self.goals = [input_list[0], input_list[1]]
        self.forbidden = input_list[2]
        self.wall = input_list[3]

        for row in range(4):
            for col in range(4):
                curTile = self.tiles[row][col]
                if (curTile.label in self.goals):
                    curTile.goal = True
                elif (curTile.label == self.forbidden):
                    curTile.forbidden = True
                
    def update_q(self, q, direction, tile_label):
        for row in range(4):
            for col in range(4):
                curTile = self.tiles[row][col]
                if (curTile.label == tile_label):
                    curTile.update_q(q, direction)
        
    def print_to_file(self):
        outF = open("board_output.txt","w")
        outF.writelines(str(self))
        outF.close()

    def __str__(self):
        tile_string = ''
        for row in range(3,-1,-1):
            for col in range(4):
                tile_string += str(self.tiles[row][col]) + '   '
            tile_string += '\n\n'
        return tile_string

def q_learn():
    randDirection = Direction(random.randrange(4))
    print(randDirection)
    print('ill learn thiz dik')

if __name__ == "__main__":

    input_list = sys.argv
    input_list.pop(0)
    board = Board(input_list)

    board.update_q(0.50, Direction.UP, 1)
    board.update_q(0.10, Direction.DOWN, 7)
    board.update_q(0.30, Direction.LEFT, 16)
    board.update_q(-0.80, Direction.RIGHT, 5)

    board.print_to_file()

    if (len(input_list) == 5) and (input_list[4] == 'p'):
        print_all_policies = True
        q_learn()
    elif (len(input_list) == 6) and (input_list[4] == 'q'):
        print_all_policies = False
        q_learn()
    else:
        print('Invalid input, please run again.')