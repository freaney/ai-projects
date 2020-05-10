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
GOAL_REWARD = 100
FORBIDDEN_REWARD = -100
GAMMA = 0.2 # Discount Rate
ALPHA = 0.1 # Learning Rate
EPSILON = 0.1 # Greedy Probability
MAX_ITERATIONS = 10000 # Will be 10,000
PRECISION_LIMIT = 0.009 # Limit of iterations
START_LABEL = 2

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
class Action(Enum):
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3
    EXIT = 4
    
    def __str__(self):
        if self.value == 0:
            return '\u2190'
        elif self.value == 1:
            return '\u2191'
        elif self.value == 2:
            return '\u2192'
        elif self.value == 3:
            return '\u2193'
        else:
            return 'X'

class Tile:
    
    def __init__(self, label, neighbors):
        '''
        Attributes:
            label (int): index of tile in visual representation of grid (1-16)
            neighbors (list[int]): labels of neighboring tiles in grid, in order [left,up,right,down]
        '''
        self.label = label
        self.neighbors = neighbors
        # Default Tile creation assumes tile is not special and has no possible actions
        # This will be changed during board creation
        self.q_values = [None]*5
        self.actions = [None]*5
        self.isGoal = False
        self.isForbidden = False
        self.isWall = False

    def get_max_q(self):
        if self.isWall:
            return 0
        else:
            return max(q for q in self.q_values if q is not None)

    def get_best_action(self):
        return Action(self.q_values.index(self.get_max_q()))

    def update_q(self, q, direction):
        self.q_values[direction.value] = q
    
    def __str__(self):
        tile_string = '[' + str(self.label) + ']:'
        for i in range(4):
            cur_q = self.q_values[i]
            if cur_q is not None:
                tile_string += str(self.q_values[i]) + '|'
            else:
                tile_string += 'n|'
        tile_string += '___'
        for action in self.actions:
            if action is not None:
                tile_string += str(action) + ','
        return tile_string

class Board:

    def __init__(self, input_list):
        self.tiles = [[1]*4 for n in range(4)]
        # tiles[row][col]
        # max_row = height - 1
        # max_col = width - 1
        # Neighbors are in order left, up, right, down
        self.tiles[0][0] = Tile(1,[None,5,2,None])
        self.tiles[0][1] = Tile(2,[1,6,3,None])
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

        self.goal_labels = [int(input_list[0]), int(input_list[1])]
        self.forbidden_label = int(input_list[2])
        self.wall_label = int(input_list[3])

        # Changes default tiles to special ones specified by user
        # Updates actions for all tiles according to available neighbors and special status 
        for row in range(4):
            for col in range(4):
                cur_tile = self.tiles[row][col]
                if (cur_tile.label in self.goal_labels):
                    cur_tile.isGoal = True
                    cur_tile.actions.insert(4,Action.EXIT)
                    cur_tile.q_values.insert(4,0)
                elif (cur_tile.label == self.forbidden_label):
                    cur_tile.isForbidden = True
                    cur_tile.actions.insert(4,Action.EXIT)
                    cur_tile.q_values.insert(4,0)
                elif (cur_tile.label == self.wall_label):
                    cur_tile.isWall = True
                else:
                    for direction_num in range(4):
                        if cur_tile.neighbors[direction_num] is not None:
                            cur_tile.actions.insert(direction_num, Action(direction_num))
                            cur_tile.q_values.insert(direction_num, 0)
                            
    def get_tile(self, label):
        for row in self.tiles:
            for tile in row:
                if (tile.label == label):
                    return tile
        print("ERROR IF TILE NOT FOUND")
    
    def update_q(self, q, direction, tile_label):
        for row in range(4):
            for col in range(4):
                cur_tile = self.tiles[row][col]
                if (cur_tile.label == tile_label):
                    cur_tile.update_q(q, direction)
        
    def print_to_file(self):
        outF = open("board_output.txt","w")
        outF.writelines(str(self))
        outF.close()

    def print_all_states(self):
        for row in self.tiles:
            for tile in row:
                best_action_str = None
                if tile.isGoal or tile.isForbidden:
                    best_action_str = 'EXIT'
                elif tile.isWall:
                    best_action_str = 'WALL'
                else:
                    best_action_str = str(tile.get_best_action())
                print(str(tile.label) + best_action_str)

    def print_tile_values(self, index):
        tile = self.get_tile(index)
        if tile.isGoal:
            print('EXIT +100')
        elif tile.isForbidden:
            print('EXIT -100')
        elif tile.isWall:
            print('WALL 0')
        else:
            for q in tile.q_values:
                if q is not None:
                    print(str(Action(tile.q_values.index(q))) + ' ' + str(q))

    def __str__(self):
        tile_string = ''
        for row in range(3,-1,-1):
            for col in range(4):
                tile_string += str(self.tiles[row][col]) + '    '
            tile_string += '\n\n'
        return tile_string

def q_learn(board, print_all_states, index):
    iterations = 0
    while (iterations < MAX_ITERATIONS):
        # Reset starting variables
        cur_tile = board.get_tile(START_LABEL)
        action = None
        exited = False
        small_iter = 0
        reward_sum = 0
        while (small_iter < 100):
            # TODO: Choose random (0.1) or calculated (0.9) action
            # Currently RANDOM
            if random.uniform(0, 1) < EPSILON:
                action = random.choice([x for x in cur_tile.actions if x is not None])          
            else:
                action = cur_tile.get_best_action()

            # Set reward
            next_tile = board.get_tile(cur_tile.neighbors[action.value])
            if next_tile.isGoal:
                reward = GOAL_REWARD
            elif next_tile.isForbidden:
                reward = FORBIDDEN_REWARD
            else:
                reward = LIVING_REWARD
            reward_sum += reward

            old_q = cur_tile.q_values[action.value]

            # Calculate and update q value
            new_q = old_q + ALPHA*(reward + GAMMA*next_tile.get_max_q() - old_q)
            cur_tile.q_values[action.value] = new_q

            if next_tile.isGoal:
                # print("GOOOOOOAAAAAAAL")
                break
            elif next_tile.isForbidden:
                # print("DEATH")
                break
            else:
                if next_tile.isWall:
                    yeet = 0
                    # print("YOU HIT A WALL")
                else:
                    cur_tile = next_tile
            small_iter += 1
        if (small_iter > 98):
            print("YOU ALMOST HAD AN INFINITE LOOP HUNNNY")
        iterations += 1
    if (print_all_states):
        board.print_all_states()
    else:
        board.print_tile_values(index)

if __name__ == "__main__":

    input_list = sys.argv
    input_list.pop(0)
    board = Board(input_list)

    board.print_to_file()

    if (len(input_list) == 5) and (input_list[4] == 'p'):
        q_learn(board, True, 0)
    elif (len(input_list) == 6) and (input_list[4] == 'q'):
        q_learn(board, False, int(input_list[5]))
    else:
        print('Invalid input, please run again.')