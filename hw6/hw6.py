import math
import sys
import random

'''
HW 6 for CISC681
@author: sfreaney@udel.edu
@updated: 5/27/2020
Linearly classifies set of 

'''

# Learning rate for logistic regression
ALPHA = 0.1

# Recursive function to calculate weights for classification using Perceptron algorithm
# Returns weights
def perceptron(input_tuples, weights, cur_iter, max_iter):

    weightsWereChanged = False

    for data in input_tuples:
        summation = 0
        actual = data[2]
        prediction = 0

        for i in range(2):
            summation += data[i]*weights[i]

        if summation >= 0:
            prediction = 1
        else:
            prediction = -1
        
        if prediction != actual:
            weightsWereChanged = True
            weights[0] += actual*data[0]
            weights[1] += actual*data[1]

    if cur_iter < max_iter and weightsWereChanged:
        cur_iter += 1
        perceptron(input_tuples, weights, cur_iter, max_iter)
    else:
        print(str(weights[0]) + ',' + str(weights[1]))

# Helper function for Logistic Regression
def sigmoid(value):
    sig = 1 / (1 + math.exp(-value))
    return sig

# Recursive function to calculate weights for classification using Binary Logistic Regression
# Returns probability of positive classification for every input
def logistic(input_tuples, weights, cur_iter, max_iter):
    weightsWereChanged = False

    for data in input_tuples:
        summation = 0
        actual = data[2]
        prediction = 0

        for i in range(2):
            summation += data[i]*weights[i]
        
        if summation >= 0:
            prediction = 1
        else:
            prediction = -1
        
        if prediction != actual:
            weightsWereChanged = True
            for i in range(2):
                weights[i] += ALPHA * data[i] * (actual - sigmoid(weights[i]))

    if cur_iter < max_iter and weightsWereChanged:
        cur_iter += 1
        logistic(input_tuples, weights, cur_iter, max_iter)
    else:
        for data in input_tuples:
            z = 0
            actual = data[2]
            prediction = 0

            for i in range(2):
                z += data[i]*weights[i]

            probability = sigmoid(z)
            print(str(probability) + ' ',end='')
        print()


if __name__ == "__main__":

    print("Please input data (NO SPACES within the triplets, please)")
    input_string = input()

    input_list = input_string.split()

    method = 'X'
    method = input_list.pop(0)

    input_string_modified = ','.join(input_list)
    input_tuples = list(eval(input_string_modified))

    if method == 'P':
        initial_weight = [0,0]
        cur_iter = 1
        max_iter = len(input_tuples)*100
        perceptron(input_tuples, initial_weight, cur_iter, max_iter)
    elif method == 'L':
        initial_weight = [0,0]
        cur_iter = 1
        max_iter = len(input_tuples)*100
        logistic(input_tuples, initial_weight, cur_iter, max_iter)
    else:
        print('Invalid input, please run again.')