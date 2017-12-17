import numpy as np
from math import *
from dynamic_function import *
import constants as consts
def simulator(model, action, delta_T, visualizer=None):
    alpha = action
    v = model.velocity
    g = consts.g
    l = model.get_l()
    I = model.I
    m = model.mass
    d = model.d

    initial_steering = model.steering_angle
    model.steering_angle = action

    time = 0.0
    while time < delta_T:
        # calculate curvature radius r and angular velocity omega
        if alpha == 0:
            r = -1
        else:
            r = d/tan(radians(alpha))
            #print("alpha",alpha,"\n")
            #print("r", r, "\n")
        omega = 0
        if (r != -1):
            omega = v/r #TODO: r = 0 and inf check
            #print("omega", omega, "\n")

        # update position and steering angle:
        model.posn += np.array([cos(radians(model.heading_angle)),\
                                sin(radians(model.heading_angle))])*v*consts.dt
        if(time == 0 and visualizer != None):
            print("omega = ", omega, "heading = ", model.heading_angle)
        model.heading_angle += degrees(omega)*consts.dt
        model.heading_angle = model.heading_angle%360
        #model.steering_angle += action / delta_T * consts.dt
        #model.steering_angle += (action-initial_steering) / delta_T * consts.dt

        # update state
        theta_doubledot = dynamicFunction(r, model) #TODO: give the fixed inputs
        if(time == 0 and visualizer != None):
            print("theta_doubledot = ", theta_doubledot)
        model.lean_angle += model.lean_angle_dot*consts.dt
        model.lean_angle_dot += degrees(theta_doubledot)*consts.dt
        time += consts.dt

        if(visualizer != None):
            visualizer(model)

    #print("r", r, "\n")
    #print("theta_doubledot", theta_doubledot, "\n")
    #print("theta_dot", theta_dot, "\n")
    #model.steering_angle = initial_steering + action # To remove numerical errors
    #model.steering_angle = action  # To remove numerical errors
    return model