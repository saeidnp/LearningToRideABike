#!/usr/bin/python3

import random
import numpy as np
import constants as consts
from state_entry import StateEntry
import visualizer
from interpolate import *
from simulator import *
from dynamic_function import *
from bicycle_model import *
import time

delta_alpha_options = np.linspace(-20,20, 25)
theta_options = np.linspace(-12,12, 17)
theta_dot_options = np.linspace(-20,20, 17)
model = BicycleModel()
Q = []


do_run = True

def reward(state):
    c = consts.c
    theta = state[0]
    theta_dot = state[1]
    return c**2 - theta**2 - (theta_dot)**2/10

def train():
    global model, Q, delta_alpha_options, theta_options, theta_dot_options
    global do_run
    if do_run == False:
        return
    cols = len(theta_options)
    rows = len(theta_dot_options)
    # value function and actions:
    Q = [ [StateEntry() for _ in range(cols)] for _ in range(rows) ]

    average_change = 10000
    iter = 0
    while average_change > 1 or iter < 10: #TODO: repeat until convergence
        Q_new = [[StateEntry() for _ in range(cols)] for _ in range(rows)]
        iter = iter+1
        average_change = 0
        print(iter)
        # choose starting state
        for theta_index in range(len(theta_options)):
            for theta_dot_index in range(len(theta_dot_options)):
                state = [theta_options[theta_index], theta_dot_options[theta_dot_index]]

                state_value = 0
                maximum = float('-inf')
                best_action = 0

                for action in delta_alpha_options:
                    theta = state[0]
                    theta_dot = state[1]
                    alpha = action
                    model.reset()
                    model.lean_angle = theta
                    model.lean_angle_dot = theta_dot
                    #model.print()
                    # get the updated model from "simulator" to get updated state
                    model = simulator(model, action, consts.dT)
                    #model.print()
                    next_state = [model.lean_angle, model.lean_angle_dot]

                    v_hat = interpolateValue(next_state, theta_options, theta_dot_options, Q)
                    if v_hat*consts.gamma >= maximum:
                        maximum = v_hat*consts.gamma
                        best_action = action
                #update the value funtion:
                Q_new[theta_dot_index][theta_index].value = reward(state) + maximum
                Q_new[theta_dot_index][theta_index].best_action = best_action
                average_change += abs(Q_new[theta_dot_index][theta_index].value - Q[theta_dot_index][theta_index].value)

        Q = Q_new
        average_change /= len(theta_dot_options) * len(theta_options)
        print("************** average_change = ", average_change, "\n")

    '''
    print("*********************************\n")
    print("-12", Q[8][0].best_action, ' ', Q[8][0].value, "\n")
    print("-6", Q[8][4].best_action, ' ', Q[8][4].value, "\n")
    print("-3", Q[8][6].best_action, ' ', Q[8][6].value, "\n")
    print("0", Q[8][8].best_action, ' ', Q[8][8].value, "\n")
    print("+3", Q[8][10].best_action, ' ', Q[8][10].value, "\n")
    print("+6", Q[8][12].best_action, ' ', Q[8][12].value, "\n")
    print("+12", Q[8][16].best_action, ' ', Q[8][16].value, "\n")

    print("*********************************\n")
    print("-12", Q[0][8].best_action, ' ', Q[8][0].value, "\n")
    print("-6", Q[4][8].best_action, ' ', Q[8][4].value, "\n")
    print("-3", Q[6][8].best_action, ' ', Q[8][6].value, "\n")
    print("0", Q[8][8].best_action, ' ', Q[8][8].value, "\n")
    print("+3", Q[10][8].best_action, ' ', Q[8][10].value, "\n")
    print("+6", Q[12][8].best_action, ' ', Q[8][12].value, "\n")
    print("+12", Q[16][8].best_action, ' ', Q[8][16].value, "\n")
    '''

def run():
    global model, Q, theta_options, theta_dot_options
    global do_run
    global run_time

    theta_index = 0
    theta_dot_index = 0
    if do_run == False:
        printf("choose theta_index:")
        print(theta_options)
        theta_index = int(input())
        printf("choose theta_dot_index:")
        print(theta_dot_options)
        theta_dot_index = int(input())
        do_run = True
        model.reset()
        model.lean_angle = theta_options[theta_index]
        model.lean_angle_dot = theta_dot_options[theta_dot_index]
        run_time = 0

    if(run_time > 50):
        do_run = False

    if(abs(model.lean_angle) > 3*consts.theta_max):
        do_run = False
        return

    action = interpolateAction([model.lean_angle, model.lean_angle_dot], theta_options, theta_dot_options, Q)
    print( "\n", "angle : ", model.lean_angle, "\t", "angle_dot : ", model.lean_angle_dot, "\t", "action : ", action)
    #simulate the bicycle for the next dT time, and visualize it.
    model = simulator(model, action, consts.dT, visualizer.SimWorld)

    run_time += consts.dT


train()

do_run = False
visualizer.start(run)
