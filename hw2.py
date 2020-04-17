import math

'''
HW 2 for CISC681
@author: sfreaney@udel.edu
@updated: 4/17/2020
Conducts alpha-beta pruning on a minimax search tree given 12 terminal node values

TO RUN:
$ python3 hw2.py
---Program will then prompt you to enter 12 terminal node values, which must be in format 'a b c d e f g h i j k m', where a-m are integers---
Then press Enter

Program will output the indices (0-11) of the terminal nodes that would be pruned by the alpha-beta pruning algorithm

Class/Method Index:
-prune(): Method used for alpha-beta pruning
-Node: Class used to create minimax tree
-__main__: Parses input string
'''
if __name__ == "__main__":  
   
    values = [3, 5, 6, 9, 1, 2, 0, -1]
    print('\nPlease input 12 terminal node values separated by spaces, then hit Enter: ')
    
    input_string = input()
    input_list = [int(num) for num in input_string.split()]

    if (len(input_list) != 12):
        print('Invalid input, please run again.')

	# # Parses input to make stack of pancakes
    # for i in range(4):
    #     size = input_list.pop(0)
    #     orientation = input_list.pop(0)
    #     pancake = [int(size), orientation]
    #     stack.append(pancake)