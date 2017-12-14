#!/usr/bin/python3

import random
import numpy as np
import simulator
import dynamic_function
import interpolate

from state_entry import StateEntry
from interpolate import *
from simulator import *
from dynamic_function import *

delta_alpha_options = np.linspace(-6,6, 9)
theta_options = np.linspace(-12,12, 17)
theta_dot_options = np.linspace(-3,3, 17)
gamma = 0.9 #or 0.8
dT = 0.4
c = 0.5 #used in reward
g = 9.8
m = 1
I = 1 #TODO: fix it
l = 0.5 #height of center of mass
v = 1
d = 0.5
position = np.array([0,0])

def reward(state):
    global c
    theta = state[0]
    return (c**2 - theta**2)

def main():
    global position, v, m, dT, g, c, gamma, l, I, d
    cols = len(theta_options)
    rows = len(theta_dot_options)
    # value function and actions:
    Q = [ [StateEntry] * cols ] * rows
    iter = 0
    while iter<10: #TODO: repeat until convergence
        iter = iter+1
        print(iter)
        theta_index = random.randint(0, len(theta_options)-1)
        theta_dot_index = random.randint(0, len(theta_dot_options)-1)
        state = [theta_options[theta_index], theta_dot_options[theta_dot_index]]
        print(state)
        state_value = 0
        maximum = float('-inf')
        best_action = 0
        for action in delta_alpha_options:
            theta = state[0]
            theta_dot = state[1]
            alpha = action
            position, alpha, next_state = simulator(alpha, state, position, v, dT,g,l,I,m,d)
            v_hat = interpolate(next_state, theta_options, theta_dot_options, Q)
            if v_hat*gamma > maximum:
                maximum = v_hat*gamma
                best_action = action
            # TODO: Compute alpha here
            #new_theta, new_theta_dot = simWorld(theta, theta_dot, alpha, dT)
        #update the value funtion:
        Q[theta_dot_index][theta_index].value = reward(state) + maximum
        Q[theta_dot_index][theta_index].best_action = best_action
main()
