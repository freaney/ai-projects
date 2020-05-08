import math
import queue

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
-prune_print_helper(): prints terminal nodes of the node-to-be-pruned
-createTree(): Creates minimax tree of depth 4
-printTree(): Prints all nodes and their properties
-Node: Class used for minimax tree
-__main__: Parses input string
'''

GOAL_HASH = '4-11'


def prune(node, alpha, beta):
    '''
    Recursively iterates through tree, calculating alpha-beta values and calling the pruning print function as needed

    Returns: value (int)
    ''' 
    if node.depth == 4:
        return node.value

    elif node.type == 'max':
        max_alpha = alpha
        # Repeat for each child 
        i = 0
        for child in node.children:
            value = prune(child, alpha, beta)  
            max_alpha = max(max_alpha, value)  
            alpha = max(alpha, max_alpha) 
            if beta <= alpha:
                if (i+1) < 2:
                    # print(child)
                    prune_print_helper(child.parent.children[i+1])
                break
            i += 1    
        return max_alpha
       
    else: 
        max_beta = beta
        j = 0
        # Repeat for each child 
        for child in node.children:          
            value = prune(child, alpha, beta) 
            max_beta = min(max_beta, value)  
            beta = min(beta, max_beta)  
            if beta <= alpha:
                if (j+1) < 2:
                    # print(child)
                    prune_print_helper(child.parent.children[j+1])
                break
            j += 1
        return max_beta
    return

# prints all child nodes of the node-to-be-pruned
def prune_print_helper(node):
    fringe = queue.Queue()
    fringe.put(node)
    visited = set()
    while not fringe.empty():
        curNode = fringe.get()
        if curNode.get_node_hash() not in visited:
            if len(curNode.children) == 0:
                print(curNode.index,end='')
                print(' ',end='')
            else:
                for child in curNode.children:
                    fringe.put(child)
                visited.add(curNode.get_node_hash())


def createTree(terminal_value_list):
    '''
    Takes list of terminal node values from user and creates minimax tree of Nodes
    The root and its immediate children are created explicitly, since the root has 3 children
    The other nodes are created in a loop since they have 2 or no children
    '''
    # Set of nodes that have already been visited
    # To be hashable, nodes are represented as a string concatenation of their depth then index separated by an underscore, which is unique
    visited = set()

    root = Node(None, list(), None)
    node2_0 = Node(root, list(), None)
    root.children.append(node2_0)
    node2_1 = Node(root, list(), None)
    root.children.append(node2_1)
    node2_2 = Node(root, list(), None)
    root.children.append(node2_2)

    created = [root, node2_0, node2_1, node2_2]
    fringe = queue.Queue()
    list(map(fringe.put, created))
    visited.add(root.get_node_hash())

    # Basically a Breadth First Search starting with the level 2 nodes
    while len(terminal_value_list) > 0:
        curNode = fringe.get()
        hashable_index =  curNode.get_node_hash()
        if hashable_index not in visited:
            if not curNode.children:
                for i in range(2):
                    child_node = Node(curNode, list(), None)
                    # If statement detecting if child leaf created is a terminal leaf
                    if (child_node.depth == 4):
                        child_node.value = terminal_value_list.pop(0)
                    curNode.children.append(child_node)
                    fringe.put(child_node)
            visited.add(curNode.get_node_hash())
    return root

# print function used for testing - will print tree starting at input node and all its subsidiaries
def printTree(root):
    fringe = queue.Queue()
    fringe.put(root)
    visited = set()
    while not fringe.empty():
        curNode = fringe.get()
        if curNode.get_node_hash() not in visited:
            print(curNode)
            if curNode.get_node_hash() == GOAL_HASH:
                print('/--STUMP--/')
                return
            else:
                for child in curNode.children:
                    fringe.put(child)
                visited.add(curNode.get_node_hash())

class Node:
    '''
    Node class used by minimax tree
    '''

    def __init__(self, parent, children, value):
        '''
		Attributes:
            parent (Node)
            children (list(Node)): list of child Nodes - root: 3 children, internal nodes: 2 children, terminal nodes: 0 children
            value (int): value at current node (will be constant for terminal nodes, and updated recursively during pruning for all other nodes)
            type (str): 'min' for minimizer node, 'max' for maximizer node
            depth (int): depth of node in tree (1-4)
            index (int): index of node at current depth (left to right, starts at 0)
        '''
        self.parent = parent
        self.children = list()

        # Assigns type, depth, index, and value
        if not self.parent:
            # Condition for root node
            self.type = 'max'
            self.depth = 1
            self.index = 0
            self.value = -math.inf
        elif self.parent.type == 'max':
            self.type =  'min'
            self.depth = self.parent.depth + 1
            self.index = len(self.parent.children) + self.parent.index*2
            self.value = math.inf
        elif self.parent.type == 'min':
            self.type = 'max'
            self.depth = self.parent.depth + 1
            self.index = len(self.parent.children) + self.parent.index*2
            self.value = -math.inf
        else:
            print('ICECREAM MACHINE BROKE')
            exit

    visited = set()    

    def get_node_hash(self):
        hashable_index = str(self.depth) + '-' + str(self.index)
        return hashable_index

    # Node string function - used for error testing
    def __str__(self):
        node_str = 'Node ' + self.get_node_hash() + '\nParent: '
        if not self.parent:
            node_str += 'PETER PAN \n'
        else:
            node_str += 'Node ' + self.parent.get_node_hash() + '\n'
        node_str += 'Children: \n'
        for child in self.children:
            node_str += '........Node ' + child.get_node_hash() + '\n'
        node_str += 'Value: ' + str(self.value) + '\nType: ' + self.type + '\n'
        return node_str

if __name__ == "__main__":
    
    print('\nPlease input 12 terminal node values separated by spaces, then hit Enter: ')
    
    input_string = input()
    input_list = [int(num) for num in input_string.split()]

    if (len(input_list) != 12):
        print('Invalid input, please run again.')
    else:
        root = createTree(input_list)
        # Initializes alpha as negative infinity and beta as positive infinity
        prune(root, -math.inf, math.inf)
        print()