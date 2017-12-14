import numpy as np
from math import *
from dynamic_function import *

def simulator(alpha, state, position, v, delta_T,g,l,I,m,d):
    # calculate curvature radius r and angular velocity alpha_dot
    if alpha == 0:
        r = -1
    else:
        r = d/tan(alpha)
    if r == -1:
        alpha_dot = 0
    else:
        alpha_dot = v/r #TODO: r = 0 and inf check

    # update position and steering angle:
    new_position = position + np.array([cos(alpha), sin(alpha)])*v*delta_T
    new_alpha = alpha + alpha_dot*delta_T

    # update state
    theta_doubledot = dynamicFunction(r,state[0],g,l,v,I,m) #TODO: give the fixed inputs
    new_theta = state[0] + state[1]*delta_T
    new_theta_dot = state[1] + theta_doubledot*delta_T
    new_state = [new_theta, new_theta_dot]

    return (new_position, new_alpha, new_state)