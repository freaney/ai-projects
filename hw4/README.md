HW 4 for CISC681
@author: sfreaney@udel.edu
@updated: 5/08/2020
Uses Q-learning algorithm to determine the best path to a goal state

TO RUN:
```python3 hw4.py```
---Program Prompt---
```# # # # X (#)``` (format explained below at !!!)
Press ```Enter```

Program will output 

!!!
Format
* Input should be in format ```#1 #2 #3 #4 p``` or ```#1 #2 #3 #4 q #5```
    * Each # is an integer in range (1,3-16) inclusive
    * #1 and #2 are goal states
    * #3 is the forbidden square
    * #4 is the wall square
    * 'p' input will print the optimal policy
    * 'q' input will print the 4 optimal Q-values at the state with index #5

Notes
s
alpha
s_prime
alpha_prime
gamma
Q(s,alpha)
R(s,alpha,s_prime)
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

Receive a sample (s,alpha,s_prime,r)
Consider old estimate Q(s,alpha)
Consider new sample estimate = R(s,a,s') + gamma*max[Q(s',a')]
Incorporate new estimate into running average