HW 4 for CISC681
@author: sfreaney@udel.edu
@updated: 5/08/2020
Uses Q-learning algorithm to determine the best path to a goal state

TO RUN:
`python3 hw4.py`
---Program Prompt---
`# # # # X (#)` (format explained below at !!!)
Press `Enter`

NOTE: Aspects of program to note
* All ties are broken in order: Left, Up, Right, Down
* 'q' option will only print values for possible actions
    * corner square will only print two actions
    * goal or forbidden square will only print the exit action
* If you would like to print the state of the board at a particular point, add `board.print_to_file()` in main or q_learn()
* Edge tiles are limited to actions within the borders
    * So if the agent is in tile 16 it cannot go up or right
    * If the agent is in tile 6, it can go in any direction, assuming it is not an exit tile or next to the wall tile
* If agent is next to wall square, it can choose action that would run it into wall square, resulting in it staying in the same square

!!!
Format
* Input should be in format `#1 #2 #3 #4 p` or `#1 #2 #3 #4 q #5`
    * Each # is an integer in range (1,3-16) inclusive
    * #1 and #2 are goal states
    * #3 is the forbidden square
    * #4 is the wall square
    * 'p' input will print the optimal policy
    * 'q' input will print the 4 optimal Q-values at the state with index #5