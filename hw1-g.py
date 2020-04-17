import math
import heapq
import queue
import copy

'''
HW 1-G for CISC681
@author: sfreaney@udel.edu
@updated: 4/10/2020
Gives solution with steps to Burnt Pancake Problem using requested search algorithm (BFS or A*)

TO RUN:
$ python3 hw1-g.py
Program will prompt you to enter the pancake sequence, which must be in format #c#c#c#c-x, where the pancake stack is read left to right
# is the pancake size (1, 2, 3, or 4), c is the side of the pancake facing up ('w' for white or 'b' for burnt), and x specifies the search algorithm ('a' for A* or 'b' for BFS)

Class/Method Index:
-astar(): Method used for A* search
-bfs(): Method used for BFS
-Node_a: Class used for A* graph with helper methods
-Node_b: Class used for BFS graph with helper methods
-__main__: Parses input string, creates root pancake stack (list), and runs user-specified search
'''

GOAL_STACK = [[1,'w'],[2,'w'],[3,'w'],[4,'w']]

def a_star(stack):
    # Initializes root with no parent, 0 location for previous flip (since no previous flip) and 0 for parent cost
    root = Node_a(stack, None, 0, 0)
    
    '''
    FRINGE
    A priority queue for nodes currently at edge of visited paths
    The root is the first node put in the fringe
    To properly order heap by minimum f(x) value (or with an enumerated stack in the case of a tie) the format of the fringe contents is (int, Node_a), where int is Node_a.f
    '''
    fringe = []
    heapq.heappush(fringe, (root.f,root))

    # Set of pancake configurations that have already been visited; to avoid graph cycles
    visited = set()

    '''
    A* Loop Functionality
    While Node_a's exist in the fringe:
    1. Pop out highest priority Node_a from fringe and label it the current Node_a.
    2. If Node_a is unvisited, goto 3. Otherwise, goto 1.
    3. If current Node_a's stack is in Goal State with minimum g, goto END.
    4. Generate all possible stacks (4) formed from flipping current stack, calculate their [g,h,f] values, and add them as Node_b's to fringe.
    5. Add current stack to set of visited Node_b's. Goto 1.
    END: Print steps from root to Goal by iteratively going through parent Node_b's. Exit loop and a_star().
    '''
    while fringe:
        curNode_a = heapq.heappop(fringe)[1]
        if str(curNode_a.stack) not in visited:
            if curNode_a.stack == GOAL_STACK:
                print('SUCCESS')
                curNode_a.print_steps()
                return
            else:
                for i in range(1,5):
                    child_stack = curNode_a.flip(i)
                    child_Node = Node_a(child_stack,curNode_a,i,curNode_a.g)
                    heapq.heappush(fringe, (child_Node.f,child_Node))
                visited.add(str(curNode_a.stack))
                
    # Only reaches this if fringe is empty, which would be an error
    print('FAILURE')

def bfs(stack):
    # Initializes root with no parents and no past flip location
    root = Node_b(stack, None, None)

    '''
    FRINGE
    A FIFO queue for nodes currently at edge of visited paths
    The root is the first node put in the fringe
    Note: The fringe may contain duplicates, but these will be identified and disregarded
    when popped off the queue to avoid loops in graph (see 'BFS Loop Functionality' below)
    '''
    fringe = queue.Queue()
    fringe.put(root)

    # Set of pancake configurations that have already been visited; to avoid graph cycles
    visited = set()    

    '''
    BFS Loop Functionality
    While Node_b's exist in the fringe:
    1. Pop out oldest Node_b from fringe and label it the current Node_b.
    2. If Node_b contains unvisited stack ordering, goto 3. Otherwise, goto 1.
    3. If current Node_b's stack is in Goal State, goto END.
    4. Generate all possible stacks (4) formed from flipping current stack and add them as Node_b's to fringe.
    5. Add current stack (as string) to set of visited Node_b's. Goto 1.
    END: Print steps from root to Goal by iteratively going through parent Node_b's. Exit loop and bfs().
    '''
    while not fringe.empty():
        curNode_b = fringe.get()
        if str(curNode_b.stack) not in visited:
            if curNode_b.stack == GOAL_STACK:
                print('SUCCESS')
                curNode_b.print_steps()
                return
            else:
                for i in range(1,5):
                    child_stack = curNode_b.flip(i)
                    fringe.put(Node_b(child_stack,curNode_b,i))
                visited.add(str(curNode_b.stack))
    # Only reaches this if fringe is empty, which would be an error
    print('FAILURE')

class Node_a:
    '''
    Node class used by a_star()
    Note:
        Pancake: Pair of attributes - size (1-4) and orientation ('b' or 'w')
    '''

    def __init__(self, stack, parent, location, parent_cost):
        '''
		Attributes:
			stack (list(list(int,str))): List of 4 Pancakes
            parent (Node_a)
            prev_flip (int): Location of spatula for flipping of parent stack to get current stack
            g (int): Cumulative cost of flips in path from root to current Node_a (backward cost)
            h (int): Heuristic that estimates closeness of current stack to goal stack by listing ID of largest pancake currently out of place/orientation (forward cost)
            f (int): A* cost, f(x), which is the sum of g(x) and h(x)
        '''
        self.stack = stack
        self.parent = parent
        self.prev_flip = location
        self.g = parent_cost + location
        self.h = self.heuristic()
        self.f = self.g + self.h

    # Returns ID of the largest pancake out of place. If in goal state, returns 0
    def heuristic(self):
        h = 0
        if (self.stack[3][0] != 4) or (self.stack[3][1] != 'w'):
            h = 4
        elif (self.stack[2][0] != 3) or (self.stack[2][1] != 'w'):
            h = 3
        elif (self.stack[1][0] != 2) or (self.stack[1][1] != 'w'):
            h = 2
        elif (self.stack[0][0] != 1) or (self.stack[0][1] != 'w'):
            h = 1
        return h

    def flip(self, location):
        '''
        Returns child stack (aka lil_stack) formed from flipping current stack at specified location
        Args:
            location (int, 1-4): spatula placement (1 is under top pancake -> 4 is under bottom pancake)
        '''
        temp_stack = copy.deepcopy(self.stack)
        lil_stack = temp_stack[:location]
        lil_stack.reverse()

        for cake in lil_stack:
            if cake[1] == 'w':
                cake[1] = 'b'
            else:
                cake[1] = 'w'
        lil_stack += temp_stack[location:]
        return lil_stack

    # Overloading the '<' operator for Nodes - used for tiebreaking in heapq
    def __lt__(self, other):

        self_num_list = copy.deepcopy(self.stack)
        other_num_list = copy.deepcopy(other.stack)

        # Convert w to 1 and b to 0       
        for i in range(4):
            if self_num_list[i][1] == 'w':
                self_num_list[i][1] = 1
            else:
                self_num_list[i][1] = 0
            if other_num_list[i][1] == 'w':
                other_num_list[i][1] = 1
            else:
                other_num_list[i][1] = 0

        # Convert 2D lists to 1D lists
        self_num_list_flat = [item for elem in self_num_list for item in elem]
        other_num_list_flat = [item for elem in other_num_list for item in elem]

        # Joining 1D int lists to single ints using string and int conversion
        self_str = [str(i) for i in self_num_list_flat] 
        self_num = int("".join(self_str))
        other_str = [str(i) for i in other_num_list_flat] 
        other_num = int("".join(other_str))

        '''
        Note: Operator is reversed. Why? Since the fringe is a min heap, it will pop
        the smallest item. If multiple Nodes have the same f value, the problem statement specifies
        that the Node with the greater numerical ID should be chosen.
        Therefore in order to return the greatest numerical ID on min heap comparison,
        '>' is used as the final comparator within the '<' overload implementation
        '''
        if (self_num > other_num): 
            return True
        else: 
            return False

    # Print function for solutions with steps from root to node
    def print_steps(self):
        print('The steps are: ')
        steps = ''
        steps = str(self) + self.print_steps_cost()
        while self.parent:
            location = self.prev_flip
            self = self.parent
            steps = self.print_steps_pipe(location) + self.print_steps_cost() + '\n' + steps
        print(steps)

    # Puts pipe character in representational pancake stack string    
    def print_steps_pipe(self, location):
        stack_str = ''
        i = 1
        for size, orientation in self.stack:
            stack_str += str(size) + orientation
            if location == i:
                stack_str += '|'
            i += 1
        return stack_str

    # Helper print function to display g and h value for each node in solution
    def print_steps_cost(self):
        cost_str = ' g=' + str(self.g) + ', h=' + str(self.h)
        return cost_str

    # Stack string function - used to create hashable item for visited set
    def __str__(self):
        stack_str = ''
        for size, orientation in self.stack:
            stack_str += str(size) + orientation
        return stack_str

class Node_b:
    '''
    Node class used by BFS
    Note:
        Pancake: Pair of attributes - size (1-4) and orientation ('b' or 'w')
    '''

    def __init__(self, stack, parent, location):
        '''
		Attributes:
			stack (list(list(int,str))): List of 4 Pancakes
            parent (Node_b)
            prev_flip (int): Location of spatula for flipping of parent stack to get current stack
        '''
        self.stack = stack
        self.parent = parent
        self.prev_flip = location

    def flip(self, location):
        '''
        Returns child stack (aka lil_stack) formed from flipping current stack at specified location,
            but only if the child stack is new
        Args:
            location (int, 1-4): spatula placement (1 is under top pancake -> 4 is under bottom pancake)
        '''
        temp_stack = copy.deepcopy(self.stack)
        lil_stack = temp_stack[:location]
        lil_stack.reverse()

        for cake in lil_stack:
            if cake[1] == 'w':
                cake[1] = 'b'
            else:
                cake[1] = 'w'
        lil_stack += temp_stack[location:]
        return lil_stack

    # Print function for solutions that lists stacks and flip locations between root and goal state
    def print_steps(self):
        print('The steps are: ')
        steps = ''
        steps = str(self)
        while self.parent:
            location = self.prev_flip
            self = self.parent
            steps = self.print_steps_helper(location) + '\n' + steps
        print(steps)

    # Puts pipe character in representational pancake stack string    
    def print_steps_helper(self, location):
        stack_str = ''
        i = 1
        for size, orientation in self.stack:
            stack_str += str(size) + orientation
            if location == i:
                stack_str += '|'
            i += 1
        return stack_str

    # Stack string function - used to create hashable item for visited set
    def __str__(self):
        stack_str = ''
        for size, orientation in self.stack:
            stack_str += str(size) + orientation
        return stack_str

if __name__ == '__main__':
    
    print('\nPlease input your pancake stack and search algorithm in #c#c#c#c-x format, then hit Enter: ')
    
    input_string = input()
    
    input_list = list(input_string)
    
    stack = list()

	# Parses input to make stack of pancakes
    for i in range(4):
        size = input_list.pop(0)
        orientation = input_list.pop(0)
        pancake = [int(size), orientation]
        stack.append(pancake)

	# Gets specified algorithm from input, which triggers the search mode called
    input_list.pop(0)
    mode = input_list.pop(0)
    if mode == 'a':
        a_star(stack)
    else:
        bfs(stack)