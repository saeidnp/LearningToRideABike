#!/usr/bin/python3

import random
import numpy as np

from state_entry import StateEntry

delta_alpha_options = np.linspace(-6,6, 9)
theta_options = np.linspace(-12,12, 17)
theta_dot_options = np.linspace(-3,3, 17)
gamma = 0.9 #or 0.8
dT = 0.4

def main():
    cols = len(theta_options)
    rows = len(theta_dot_options)
    a = [ [StateEntry] * cols ] * rows
    iter = 0
    while True:
        iter = iter+1
        print(iter)
        state = [random.choice(theta_options), random.choice(theta_dot_options)]
        print(state)
        state_best_action = 0
        state_value = 0
        for action in delta_alpha_options:
            theta = state[0]
            theta_dot = state[1]
            alpha = 0
            # TODO: Compute alpha here
            #new_theta, new_theta_dot = simWorld(theta, theta_dot, alpha, dT)

main()
